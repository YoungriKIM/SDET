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
# 3 | 스파이크 테스트 코드 (순간적인 과부하 발생!)
TEST_URL = "http://127.0.0.1:5000/test"
BASE_CONCURRENT_REQUESTS = 10  # 평소 동시 요청 개수
SPIKE_REQUESTS = 100  # 스파이크 발생 시 동시 요청 개수
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
# 기본 부하 (평소 트래픽 수준)
print("\n# 기본 부하 상태 (일반적인 사용량)")
with ThreadPoolExecutor(max_workers=BASE_CONCURRENT_REQUESTS) as executor:
    results = list(executor.map(lambda _: send_request(), range(TOTAL_REQUESTS)))

success_responses = [duration for status, duration in results if status == 200]
if success_responses:
    avg_response_time = sum(success_responses) / len(success_responses)
    print(f"O | 평균 응답 시간: {avg_response_time:.2f}s")

# ---------------------------------------------------------------------------------
# 스파이크 부하 발생 (순간적으로 트래픽 폭발!)
print("\n# 스파이크 테스트 시작 (순간적인 트래픽 폭발)")
with ThreadPoolExecutor(max_workers=SPIKE_REQUESTS) as executor:
    results = list(executor.map(lambda _: send_request(), range(TOTAL_REQUESTS)))

# 응답 시간 분석
success_responses = [duration for status, duration in results if status == 200]
error_responses = [status for status, _ in results if status == "ERROR"]

if success_responses:
    avg_response_time = sum(success_responses) / len(success_responses)
    print(f"O | 평균 응답 시간: {avg_response_time:.2f}s")

if error_responses:
    print(f"X | 오류 발생! {len(error_responses)}개의 요청이 실패함.")

print("\n# 스파이크 테스트 완료!")
