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
    time.sleep(0.5)  # 응답 지연 추가 (0.5초)
    return jsonify({"message": "테스트 응답 완료!"})

def run_server(): # 서버 실행
    app.run(debug=True, use_reloader=False, port=5000)
    
# ---------------------------------------------------------------------------------
# 2 | 백그라운드에서 flask 서버 실행
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# ---------------------------------------------------------------------------------
# 3 | 부하 테스트 코드 (점진적 부하 증가)
TEST_URL = "http://127.0.0.1:5000/test"  # 테스트할 API
MAX_CONCURRENT_REQUESTS = 50  # 최대 동시 요청 개수
STEP = 10  # 한 단계씩 증가할 요청 개수
TOTAL_REQUESTS = 100  # 전체 요청 개수

def send_request():
    start_time = time.time()
    response = requests.get(TEST_URL)
    end_time = time.time()
    
    return response.status_code, round(end_time - start_time, 2)

# 서버 실행될 시간 주고
time.sleep(1)

# ---------------------------------------------------------------------------------
# 점진적으로 부하 증가시키면서 테스트
print("\n# 점진적 부하 테스트 시작!")
for concurrent_requests in range(STEP, MAX_CONCURRENT_REQUESTS + 1, STEP):
    print(f"\n동시 요청 개수: {concurrent_requests}")
    
    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        results = list(executor.map(lambda _: send_request(), range(TOTAL_REQUESTS)))

    # 결과 출력
    avg_response_time = sum(duration for _, duration in results) / len(results)
    print(f"평균 응답 시간: {avg_response_time:.2f}s")

print("\n부하 테스트 완료!")