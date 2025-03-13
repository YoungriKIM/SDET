from flask import Flask, jsonify
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# 1 | Flask 서버 설정
app = Flask(__name__)

@app.route('/fast') # 즉시 응답하는 엔드포인트
def fast_response():
    return jsonify({"message": "빠른 응답!"})

@app.route('/slow')
def slow_response():
    time.sleep(1) # 1초의 응답 지연
    return jsonify({"message": "1초가 소요되는 응답!"})

def run_server(): # 서버 실행
    app.run(debug=True, use_reloader=False, port=5000)
    
# ---------------------------------------------------------------------------------
# 2 | 백그라운드에서 flask 서버 실행
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# ---------------------------------------------------------------------------------
# 3 | 성능 테스트 코드(부하 테스트)
FAST_URL = "http://127.0.0.1:5000/fast" # 테스트 할 API
SLOW_URL = "http://127.0.0.1:5000/slow" # 테스트 할 API
NUM_REQUESTS = 24 # 보낼 요청 수
CONCURRENT_REQUESTS = 10 # 동시 요청 개수

def send_request(URL):
    start_time = time.time()
    response = requests.get(URL)
    end_time = time.time()
    
    return response.status_code, round(end_time - start_time, 2)

# 서버 실행될 시간 주고
time.sleep(1)

# ---------------------------------------------------------------------------------
# 병렬 요청 실행 - fast
print("# /fast API 성능 테스트 시작")
with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
    results = list(executor.map(send_request, [FAST_URL] * NUM_REQUESTS))
# 결과 출력
for i, (status, duration) in enumerate(results):
    print(f"Request {i+1}: Status {status}, Response time {duration}s")
    
# 병렬 요청 실행 - slow
print("# /slow API 성능 테스트 시작")
with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
    results = list(executor.map(send_request, [SLOW_URL] * NUM_REQUESTS))
# 결과 출력
for i, (status, duration) in enumerate(results):
    print(f"Request {i+1}: Status {status}, Response time {duration}s")