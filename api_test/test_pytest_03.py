# API 사용한 특정 상품 존재 확인 (fakestoreapi)
import requests

def test_product_list_contains_item():
    # 상품 정보 가져오기(GET)
    store_url = "https://fakestoreapi.com/products"
    res = requests.get(store_url)
    
    assert res.status_code == 200
    product_list = res.json()
    assert isinstance(product_list, list)
    assert len(product_list) > 0
    
    # 특정 상품 제목 포함 여부
    matched = [p for p in product_list if "Fjallraven" in p['title']]
    assert len(matched) > 0
