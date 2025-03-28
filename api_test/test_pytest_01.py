# 파일명 규칙
    # 파일명: test_*.py
    # 함수명: def test_*():
    
# 아래 총 함수 17개 파일을 "pytest {이 파일 경로}.py" 로 실행하면
    # 1개 무시됨
    # 1개 실패
    # 15개 성공
    
def diff_name(): #함수명 규칙 다를 시 인식 안 함
    assert True is True

# 비교 연산자
def test_equal():
    assert 2 + 2 == 4
    
def test_not_equal():
    assert 2 * 2 != 5
    
def test_greater_than():
    assert 10 > 9
    
def test_greater_equal():
    assert 10 >= 10
    
def test_less_than():
    assert 0 < 5
    
def test_less_equal():
    assert 5 <= 6

# 논리 연산자
def test_and():
    assert 1 < 5 and 5 < 10 and 'a' == 'a'
    
def test_or():
    assert 'ttotto' == 'ttotto' or 10 == 100
    
def test_not():
    assert not False
    
# in / not in
def test_in_list():
    assert 3 in [1,2,3,4,5]
    
def test_in_string():
    assert 't' in 'ttotto'
    
def test_not_in():
    assert 'cat' not in ['hamster', 'dog']
    
# 자료형 관련
def test_list_length():
    my_list = [1,2,3]
    assert len(my_list) == 3
    
def test_dict_key_check():
    my_dict = {'name':'ttotto', 'job':'QA'}
    assert 'job' in my_dict
    
def test_type_check():
    assert isinstance(123, int)
    
# 실패 해보기
def test_fail_example():
    assert 999 == 1000