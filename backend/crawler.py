"""
편의점 행사 상품 (1+1, 2+1) 수집 엔진 & 데이터 정규화 모듈
- 대상 편의점: GS25, CU, 세븐일레븐, 이마트24
- 기능: 행사 데이터 구조화, 개당 단가 자동 산출, 매장별 모의 실시간 재고 생성
"""

import json
import os
import random
from datetime import datetime

# 데이터 저장 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "cvs_data.json")

# 편의점 브랜드 정의
BRANDS = {
    "GS25": {"color": "#0072CE", "bg": "rgba(0, 114, 206, 0.15)", "logo": "GS25"},
    "CU": {"color": "#652D90", "bg": "rgba(101, 45, 144, 0.15)", "logo": "CU"},
    "7-ELEVEN": {"color": "#00805A", "bg": "rgba(0, 128, 90, 0.15)", "logo": "7-ELEVEN"},
    "EMART24": {"color": "#FFB81C", "bg": "rgba(255, 184, 28, 0.15)", "logo": "이마트24"}
}

# 카테고리 정의
CATEGORIES = ["음료/커피", "스낵/과자", "라면/간편식", "디저트/베이커리", "신선식품", "생활용품"]

# 대표 행사 상품 템플릿 데이터 (4대 편의점 실제 대표 행사 리스트 기반)
SAMPLE_PRODUCTS = [
    # 음료
    {"name": "코카콜라 제로 500ml", "brand": "GS25", "price": 2300, "event_type": "1+1", "category": "음료/커피", "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "칠성사이다 제로 500ml", "brand": "CU", "price": 2200, "event_type": "1+1", "category": "음료/커피", "image": "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=300"},
    {"name": "몬스터에너지 울트라 355ml", "brand": "7-ELEVEN", "price": 2300, "event_type": "2+1", "category": "음료/커피", "image": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=300"},
    {"name": "조지아 크래프트 아메리카노 470ml", "brand": "EMART24", "price": 2500, "event_type": "1+1", "category": "음료/커피", "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=300"},
    {"name": "비타500 100ml 10입", "brand": "GS25", "price": 9000, "event_type": "1+1", "category": "음료/커피", "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=300"},
    {"name": "빙그레 바나나맛우유 240ml", "brand": "CU", "price": 1700, "event_type": "2+1", "category": "음료/커피", "image": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300"},

    # 디저트 & 베이커리
    {"name": "연세우유 생크림빵", "brand": "CU", "price": 2800, "event_type": "2+1", "category": "디저트/베이커리", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"},
    {"name": "혜자로운 집밥 제육볶음 도시락", "brand": "GS25", "price": 4500, "event_type": "1+1", "category": "신선식품", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300"},
    {"name": "삼립 돌아온 포켓몬빵 꼬부기빵", "brand": "7-ELEVEN", "price": 1500, "event_type": "1+1", "category": "디저트/베이커리", "image": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},
    {"name": "노브랜드 버터쿠키 400g", "brand": "EMART24", "price": 3480, "event_type": "1+1", "category": "스낵/과자", "image": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},

    # 스낵 & 라면
    {"name": "포카칩 원조감자맛 66g", "brand": "GS25", "price": 1700, "event_type": "2+1", "category": "스낵/과자", "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=300"},
    {"name": "허니버터칩 60g", "brand": "CU", "price": 1700, "event_type": "2+1", "category": "스낵/과자", "image": "https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=300"},
    {"name": "신라면 큰사발", "brand": "7-ELEVEN", "price": 1400, "event_type": "2+1", "category": "라면/간편식", "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=300"},
    {"name": "불닭볶음면 큰사발", "brand": "EMART24", "price": 1800, "event_type": "1+1", "category": "라면/간편식", "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},
    {"name": "오뚜기 진라면 매운맛 큰사발", "brand": "GS25", "price": 1400, "event_type": "2+1", "category": "라면/간편식", "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},
    {"name": "하리보 골드베렌 100g", "brand": "CU", "price": 2000, "event_type": "1+1", "category": "스낵/과자", "image": "https://images.unsplash.com/photo-1582058091505-f87a2e55a40f?w=300"},
    
    # 생활용품
    {"name": "질레트 마하3 면도날 4입", "brand": "7-ELEVEN", "price": 18900, "event_type": "1+1", "category": "생활용품", "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=300"},
    {"name": "페브리즈 깨끗한상쾌한향 370ml", "brand": "EMART24", "price": 8900, "event_type": "1+1", "category": "생활용품", "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "크리넥스 수프림소프트 3겹 30롤", "brand": "GS25", "price": 28900, "event_type": "1+1", "category": "생활용품", "image": "https://images.unsplash.com/photo-1584556812952-905ffd0c611a?w=300"},
    {"name": "리스테린 쿨미놀 750ml", "brand": "CU", "price": 9500, "event_type": "1+1", "category": "생활용품", "image": "https://images.unsplash.com/photo-1559598467-f8b76c8155d0?w=300"}
]

# 모의 매장 위치 데이터 (강남, 홍대, 부산 해운대, 명동 중심가 클러스터)
STORES_SAMPLE = [
    # 강남권역
    {"id": "S001", "name": "GS25 강남역점", "brand": "GS25", "lat": 37.4979, "lng": 127.0276, "address": "서울특별시 강남구 테헤란로 101", "open24": True},
    {"id": "S002", "name": "CU 강남센트럴점", "brand": "CU", "lat": 37.4988, "lng": 127.0288, "address": "서울특별시 강남구 강남대로 390", "open24": True},
    {"id": "S003", "name": "세븐일레븐 강남포스코점", "brand": "7-ELEVEN", "lat": 37.4965, "lng": 127.0260, "address": "서울특별시 강남구 역삼로 108", "open24": False},
    {"id": "S004", "name": "이마트24 강남역플래그십", "brand": "EMART24", "lat": 37.4995, "lng": 127.0265, "address": "서울특별시 강남구 테헤란로 115", "open24": True},

    # 홍대/신촌권역
    {"id": "S005", "name": "CU 홍대입구역점", "brand": "CU", "lat": 37.5563, "lng": 126.9226, "address": "서울특별시 마포구 양화로 160", "open24": True},
    {"id": "S006", "name": "GS25 홍대상상마당점", "brand": "GS25", "lat": 37.5509, "lng": 126.9214, "address": "서울특별시 마포구 어울마당로 65", "open24": True},
    {"id": "S007", "name": "세븐일레븐 홍대걷고싶은거리점", "brand": "7-ELEVEN", "lat": 37.5540, "lng": 126.9240, "address": "서울특별시 마포구 홍익로 15", "open24": True},
    {"id": "S008", "name": "이마트24 신촌역점", "brand": "EMART24", "lat": 37.5552, "lng": 126.9368, "address": "서울특별시 서대문구 신촌로 99", "open24": False},

    # 광화문/명동권역
    {"id": "S009", "name": "GS25 광화문S타워점", "brand": "GS25", "lat": 37.5700, "lng": 126.9770, "address": "서울특별시 종로구 세종대로 149", "open24": True},
    {"id": "S010", "name": "CU 명동본점", "brand": "CU", "lat": 37.5635, "lng": 126.9837, "address": "서울특별시 중구 명동8길 27", "open24": True},
    {"id": "S011", "name": "세븐일레븐 종로3가점", "brand": "7-ELEVEN", "lat": 37.5704, "lng": 126.9912, "address": "서울특별시 종로구 수표로 105", "open24": True},

    # 부산 해운대권역
    {"id": "S012", "name": "GS25 해운대구남로점", "brand": "GS25", "lat": 35.1601, "lng": 129.1608, "address": "부산광역시 해운대구 구남로 21", "open24": True},
    {"id": "S013", "name": "CU 해운대비치점", "brand": "CU", "lat": 35.1588, "lng": 129.1625, "address": "부산광역시 해운대구 해운대해변로 265", "open24": True}
]

def calculate_unit_price(price: int, event_type: str) -> float:
    """행사 종류에 따른 1개당 실질 단가 산출"""
    if event_type == "1+1":
        return round(price / 2, 1)
    elif event_type == "2+1":
        return round((price * 2) / 3, 1)
    return float(price)

def process_and_normalize_data():
    """행사 상품 데이터 생성 및 1개당 단가 계산, 모의 실시간 재고 바인딩"""
    products = []
    
    # 1. 상품 정규화 데이터 생성
    for idx, prod in enumerate(SAMPLE_PRODUCTS, 1):
        unit_price = calculate_unit_price(prod["price"], prod["event_type"])
        discount_rate = round((1 - (unit_price / prod["price"])) * 100)
        
        products.append({
            "id": f"P{idx:03d}",
            "name": prod["name"],
            "brand": prod["brand"],
            "price": prod["price"],
            "unit_price": unit_price,
            "discount_rate": discount_rate,
            "event_type": prod["event_type"],
            "category": prod["category"],
            "image": prod["image"],
            "updated_at": datetime.now().strftime("%Y-%m-01 00:00:00") # 월초 갱신 표현
        })

    # 2. 매장별 모의 실시간 재고 (POS 동기화 모사) 생성
    stores = []
    for store in STORES_SAMPLE:
        brand_products = [p for p in products if p["brand"] == store["brand"]]
        
        inventory = []
        for p in brand_products:
            qty = random.choice([0, 1, 2, 3, 4, 5, 8])
            inventory.append({
                "product_id": p["id"],
                "product_name": p["name"],
                "event_type": p["event_type"],
                "price": p["price"],
                "unit_price": p["unit_price"],
                "category": p["category"],
                "stock_quantity": qty,
                "is_in_stock": qty > 0,
                "last_pos_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
        stores.append({
            **store,
            "inventory": inventory,
            "total_event_items": len(inventory),
            "in_stock_items": sum(1 for i in inventory if i["is_in_stock"])
        })

    full_dataset = {
        "metadata": {
            "version": "1.0.0",
            "last_crawled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_products": len(products),
            "total_stores": len(stores),
            "brands": list(BRANDS.keys())
        },
        "brands": BRANDS,
        "categories": CATEGORIES,
        "products": products,
        "stores": stores
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(full_dataset, f, ensure_ascii=False, indent=2)

    print(f"[OK] Data pipeline created! Total {len(products)} products, {len(stores)} stores processed.")
    return full_dataset

if __name__ == "__main__":
    process_and_normalize_data()
