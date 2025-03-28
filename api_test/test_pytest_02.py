# API 사용한 로그인, 유저 정보 확인 테스트

import requests

def test_login_and_get_user():
    # 로그인(POST)
    login_url = "https://reqres.in/api/login"
    login_payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    
    login_res = requests.post(login_url, json = login_payload)
    assert login_res.status_code == 200
    token = login_res.json().get("token")
    assert token is not None
    
    # 사용자 조회(GET)
    user_url = "https://reqres.in/api/users/2"
    user_res = requests.get(user_url)
    assert user_res.status_code == 200
    user_data = user_res.json().get("data")
    assert user_data["id"] == 2
    assert "email" in user_data