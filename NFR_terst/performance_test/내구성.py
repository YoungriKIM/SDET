from flask import Flask, jsonify
import threading
import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor
import logging

# Flask 기본 로그를 최소화 (WARNING 이상만 출력)
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

# ---------------------------------------------------------------------------------
# 1 | Flask 서버 설정 및 API 만들기
app = Flask(__name__)

@app.route('/test')  # 테스트용 엔드포인트
def test_response():
    delay = random.uniform(0.5, 1.5)  # 0.5~1.5초 랜덤 딜레이 (서버 부하 시뮬레이션)
    time.sleep(delay)
    return jsonify({"message": "테스트 응답 완료!", "delay": round(delay, 2)})

def run_server():  # 서버 실행
    app.run(debug=True, use_reloader=False, port=5000)

# ---------------------------------------------------------------------------------
# 2 | 백그라운드에서 Flask 서버 실행
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# ---------------------------------------------------------------------------------
# 3 | 내구성 테스트 코드 (오랜 시간 지속 부하!)
TEST_URL = "http://127.0.0.1:5000/test"
CONCURRENT_REQUESTS = 20  # 동시 요청 개수 (적정 수준 유지)
DURATION = 10 * 60  # 10분 동안 테스트 (단위: 초)
INTERVAL = 5  # 5초마다 부하 테스트 진행
TOTAL_REQUESTS = 100  # 한 번 실행할 때 보낼 요청 개수

def send_request():
    start_time = time.time()
    try:
        response = requests.get(TEST_URL, timeout=10)  # 타임아웃 10초 설정
        end_time = time.time()
        return response.status_code, round(end_time - start_time, 2)
    except requests.exceptions.RequestException:
        return "ERROR", -1  # 요청 실패 처리

# 서버 실행될 시간 주기
time.sleep(1)

# ---------------------------------------------------------------------------------
# 일정 시간 동안 지속적인 부하 실행
print("\n# 내구성 테스트 시작! (테스트 시간: 10분)")

start_time = time.time()
while time.time() - start_time < DURATION:
    print(f"\n > {round(time.time() - start_time, 2)}초 경과 - 요청 실행 중...")
    
    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        results = list(executor.map(lambda _: send_request(), range(TOTAL_REQUESTS)))

    # 응답 시간 분석
    success_responses = [duration for status, duration in results if status == 200]
    error_responses = [status for status, _ in results if status == "ERROR"]

    if success_responses:
        avg_response_time = sum(success_responses) / len(success_responses)
        print(f"O | 평균 응답 시간: {avg_response_time:.2f}s")
    
    if error_responses:
        print(f"X | 오류 발생! {len(error_responses)}개의 요청이 실패함.")

    # INTERVAL 시간 동안 기다렸다가 다시 요청 (오랜 시간 지속 부하 시뮬레이션)
    time.sleep(INTERVAL)

print("\n# 내구성 테스트 완료!")
