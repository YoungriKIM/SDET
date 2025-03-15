from flask import Flask, jsonify
import threading
import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor
import logging

# Flask 기본 로그를 최소화 (INFO 이상 로그만 출력)
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)  # WARNING 이상만 출력 (ERROR만 보고 싶다면 'ERROR'로 변경)

# ---------------------------------------------------------------------------------
# 1 | Flask 서버 설정 및 API 만들기
app = Flask(__name__)

@app.route('/test')  # 테스트용 엔드포인트
def test_response():
    delay = random.uniform(0.5, 2.0)  # 0.5초 ~ 2초 랜덤 딜레이
    time.sleep(delay)
    return jsonify({"message": "테스트 응답 완료!", "delay": round(delay, 2)})

def run_server():  # 서버 실행
    app.run(debug=True, use_reloader=False, port=5000)

# ---------------------------------------------------------------------------------
# 2 | 백그라운드에서 flask 서버 실행
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# ---------------------------------------------------------------------------------
# 3 | 스트레스 테스트 코드 (한계를 넘는 부하)
TEST_URL = "http://127.0.0.1:5000/test"  # 테스트할 API
START = 60  # 60부터 서버 성능 저하를 부하 테스트에서 미리 확인
STEP = 20  # 한 번에 증가할 요청 개수
MAX_CONCURRENT_REQUESTS = 200  # 동시 요청 최대 개수
TOTAL_REQUESTS = 300  # 전체 요청 개수

def send_request():
    start_time = time.time()
    try:
        response = requests.get(TEST_URL, timeout=10)  # 타임아웃 10초 설정
        end_time = time.time()
        return response.status_code, round(end_time - start_time, 2)
    except requests.exceptions.RequestException:
        return "ERROR", -1  # 요청 실패 처리

# 서버 실행될 시간 주고
time.sleep(1)

# ---------------------------------------------------------------------------------
# 점진적으로 부하 증가기키고 한계 초과 시 서버 반응 확인
print("\n#스트레스 테스트 시작!")
for concurrent_requests in range(START, MAX_CONCURRENT_REQUESTS + 1, STEP):
    print(f"\n동시 요청 개수: {concurrent_requests}")
    
    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        results = list(executor.map(lambda _: send_request(), range(TOTAL_REQUESTS)))

    # 응답 시간 분석
    success_responses = [duration for status, duration in results if status == 200]
    error_responses = [status for status, _ in results if status == "ERROR"]

    if success_responses:
        avg_response_time = sum(success_responses) / len(success_responses)
        print(f"O | 평균 응답 시간: {avg_response_time:.2f}s")
    
    if error_responses:
        print(f"X | 오류 발생! {len(error_responses)}개의 요청이 실패함.")

    # 특정 임계치에서 중단 (예: 50% 이상 오류 발생 시)
    if len(error_responses) > TOTAL_REQUESTS * 0.5:
        print("서버가 과부하 상태, 테스트 진행 불가.")
        break

print("\n# 스트레스 테스트 완료!")
