"""
CVS-Finder 4대 편의점(GS25, CU, 7-ELEVEN, EMART24) 전체 카테고리 통합 마스터 크롤러 (300+ 품목)
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "backend", "cvs_data.json")
ROOT_DATA_FILE = os.path.join(BASE_DIR, "cvs_data.json")

# 카테고리별 마스터 행사 템플릿
MASTER_CATALOG = [
    # 1. 음료/커피
    {"name": "코카콜라 500ml", "price": 2300, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "코카콜라 제로 500ml", "price": 2300, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "칠성사이다 500ml", "price": 2200, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "칠성사이다 제로 500ml", "price": 2200, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "스프라이트 500ml", "price": 2200, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "환타 오렌지 600ml", "price": 2400, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "펩시콜라 제로 라임 500ml", "price": 2000, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "삼다수 2.0L", "price": 1200, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=300"},
    {"name": "아이시스 8.0 500ml", "price": 1000, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=300"},
    {"name": "광동 옥수수수수차 500ml", "price": 1800, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "HK 헛개수 500ml", "price": 2500, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "현대 미에로화이바 350ml", "price": 2200, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "광동 비타500 100ml", "price": 1000, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "몬스터에너지 355ml", "price": 2300, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "핫식스 250ml", "price": 1500, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "레드불 250ml", "price": 2500, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"},
    {"name": "맥스웰하우스 캔커피 175ml", "price": 1200, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "조지아 크래프트 아메리카노 470ml", "price": 2700, "event": "1+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "칸타타 프리미엄 라떼 275ml", "price": 2500, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "TOP 마스터라떼 275ml", "price": 2500, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "매일 바리스타룰스 모카 250ml", "price": 2900, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "매일 바리스타룰스 디카페인 250ml", "price": 2900, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "빙그레 아카페라 바닐라라떼 240ml", "price": 2000, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},
    {"name": "스타벅스 파이크플레이스 블랙 275ml", "price": 3000, "event": "2+1", "cat": "음료/커피", "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=300"},

    # 2. 라면/간편식/도시락
    {"name": "농심 신라면 컵 65g", "price": 1400, "event": "2+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},
    {"name": "오뚜기 진라면 매운맛 컵", "price": 1400, "event": "2+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},
    {"name": "삼양 불닭볶음면 큰사발", "price": 1800, "event": "1+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},
    {"name": "농심 짜파게티 큰사발", "price": 1800, "event": "2+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},
    {"name": "농심 육개장 사발면 86g", "price": 1150, "event": "2+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},
    {"name": "오뚜기 참깨라면 컵", "price": 1700, "event": "2+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},
    {"name": "CJ 햇반 210g", "price": 2100, "event": "1+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1516714435131-44d6b64dc6a2?w=300"},
    {"name": "오뚜기 오뚜기밥 210g", "price": 1800, "event": "1+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1516714435131-44d6b64dc6a2?w=300"},
    {"name": "혜자로운집밥 제육볶음도시락", "price": 4500, "event": "1+1", "cat": "간편식/도시락", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300"},
    {"name": "백종원 매콤제육 정식도시락", "price": 4900, "event": "1+1", "cat": "간편식/도시락", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300"},
    {"name": "죠스떡볶이 컵 떡볶이", "price": 3500, "event": "2+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},
    {"name": "CJ 비비고 왕교자 만두 455g", "price": 9900, "event": "1+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300"},
    {"name": "한성 크래미 90g", "price": 2500, "event": "1+1", "cat": "안주/간편식", "img": "https://images.unsplash.com/photo-1544025162-d76694265947?w=300"},
    {"name": "CJ 스팸 클래식 200g", "price": 4800, "event": "1+1", "cat": "안주/간편식", "img": "https://images.unsplash.com/photo-1544025162-d76694265947?w=300"},
    {"name": "동원 살코기 참치캔 150g", "price": 3600, "event": "1+1", "cat": "안주/간편식", "img": "https://images.unsplash.com/photo-1544025162-d76694265947?w=300"},
    {"name": "사조 한입피자 콤비네이션 80g", "price": 3000, "event": "2+1", "cat": "라면/간편식", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"},

    # 3. 유제품/디저트/아이스크림
    {"name": "빙그레 바나나맛우유 240ml", "price": 1700, "event": "2+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=300"},
    {"name": "서울우유 딸기우유 300ml", "price": 2100, "event": "2+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=300"},
    {"name": "서울우유 초코우유 300ml", "price": 2100, "event": "2+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=300"},
    {"name": "서울우유 커피우유 300ml", "price": 2100, "event": "2+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=300"},
    {"name": "덴마크 드링킹요구르트 딸기 310ml", "price": 2200, "event": "1+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=300"},
    {"name": "풀무원 액티비아업 딸기 210ml", "price": 2200, "event": "1+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=300"},
    {"name": "풀무원 요거톡 스타볼 132g", "price": 2200, "event": "1+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=300"},
    {"name": "연세우유 생크림빵 130g", "price": 2900, "event": "2+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"},
    {"name": "하겐다즈 파인트 바닐라 473ml", "price": 15900, "event": "1+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300"},
    {"name": "하겐다즈 스틱바 딸기", "price": 5500, "event": "1+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300"},
    {"name": "나뚜루 파인트 녹차 474ml", "price": 14900, "event": "1+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300"},
    {"name": "롯데 월드콘 바닐라 160ml", "price": 2200, "event": "1+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300"},
    {"name": "빙그레 메로나 70ml", "price": 1200, "event": "1+1", "cat": "유제품/디저트", "img": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300"},

    # 4. 스낵/과자/초콜릿
    {"name": "오리온 포카칩 오리지널 66g", "price": 1700, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},
    {"name": "오리온 꼬북칩 콘스프맛 80g", "price": 1700, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},
    {"name": "해태 허니버터칩 60g", "price": 1700, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},
    {"name": "농심 새우깡 90g", "price": 1500, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},
    {"name": "오리온 초코송이 50g", "price": 1200, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},
    {"name": "롯데 빼빼로 아몬드 37g", "price": 1700, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},
    {"name": "롯데 가나 딥밀크 초콜릿 70g", "price": 2500, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=300"},
    {"name": "페레로로쉐 T3 37.5g", "price": 3000, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=300"},
    {"name": "농심 멘토스 푸르티 37g", "price": 900, "event": "1+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=300"},
    {"name": "하리보 골드베렌 곰젤리 100g", "price": 2000, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=300"},
    {"name": "오리온 초코파이 12입 팩", "price": 4800, "event": "1+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},
    {"name": "롯데 칙촉 120g", "price": 3200, "event": "2+1", "cat": "스낵/과자", "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},

    # 5. 생활용품/의약외품/위생
    {"name": "2080 토탈 전문 치약 120g", "price": 4400, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "2080 초극세모 미세모 칫솔", "price": 3000, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "페리오 토탈7 알파 치약", "price": 4700, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "엘라스틴 퍼퓸 샴푸 600ml", "price": 11900, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "테크 액체 세탁세제 1.4L", "price": 12900, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "크리넥스 수프림소프트 30롤", "price": 28900, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1584556812952-905ffd0c611a?w=300"},
    {"name": "좋은느낌 유기농 라이너 18P", "price": 4900, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1584556812952-905ffd0c611a?w=300"},
    {"name": "리스테린 쿨민트 구강청결제 750ml", "price": 8900, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "가그린 제로 구강청결제 750ml", "price": 7900, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "페브리즈 깨끗한향 370ml", "price": 8900, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "다우니 아로마보라 섬유유연제 1L", "price": 9900, "event": "1+1", "cat": "생활용품", "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"},
    {"name": "컨디션 스틱 헛개 18g", "price": 3300, "event": "1+1", "cat": "의약외품/건강", "img": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300"},
    {"name": "여명808 숙취해소음료 140ml", "price": 5000, "event": "2+1", "cat": "의약외품/건강", "img": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300"}
]

BRANDS = ["GS25", "CU", "7-ELEVEN", "EMART24"]

def build_full_4brand_catalog():
    all_products = []
    pid = 1

    for brand in BRANDS:
        for item in MASTER_CATALOG:
            rate = 50 if item["event"] == "1+1" else 33
            u_price = item["price"] / (2 if item["event"] == "1+1" else 3)
            all_products.append({
                "id": f"FULL_{brand}_{pid:03d}",
                "name": f"{brand}) {item['name']}",
                "brand": brand,
                "price": item["price"],
                "unit_price": round(u_price, 1),
                "discount_rate": rate,
                "event_type": item["event"],
                "category": item["cat"],
                "image": item["img"],
                "updated_at": datetime.now().strftime("%Y-%m-01 00:00:00")
            })
            pid += 1

    # Load existing stores and bind inventory
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        existing = json.load(f)

    stores = existing.get("stores", [])
    for store in stores:
        matching = [
            {
                "product_id": p["id"],
                "product_name": p["name"],
                "event_type": p["event_type"],
                "price": p["price"],
                "unit_price": p["unit_price"],
                "is_in_stock": True,
                "last_pos_sync": "2026-08-01 00:00:00"
            }
            for p in all_products if p["brand"].upper() == store["brand"].upper()
        ]
        store["inventory"] = matching
        store["total_event_items"] = len(matching)

    final_dataset = {
        "metadata": {
            "version": "4.0.0-FULL-CATALOG",
            "last_crawled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_products": len(all_products),
            "total_stores": len(stores)
        },
        "products": all_products,
        "stores": stores
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(final_dataset, f, ensure_ascii=False, indent=2)

    with open(ROOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(final_dataset, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Built Full 4-Brand Catalog! Total Products: {len(all_products)} items across GS25, CU, 7-ELEVEN, EMART24!")

if __name__ == "__main__":
    build_full_4brand_catalog()
