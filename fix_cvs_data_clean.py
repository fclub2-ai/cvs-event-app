"""
Fix cvs_data.json stores once and for all.
Ensure 100% matching brand, name, address, lat, lng, and inventory without ANY mismatch.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "backend", "cvs_data.json")
ROOT_DATA_FILE = os.path.join(BASE_DIR, "cvs_data.json")

PRECISE_STORES_CLEAN = [
    {
        "id": "ST001",
        "name": "CU 신촌로터리점",
        "brand": "CU",
        "lat": 37.5552,
        "lng": 126.9368,
        "address": "서울특별시 서대문구 신촌로 92 (신촌역 7번 출구 앞)",
        "open24": True
    },
    {
        "id": "ST002",
        "name": "GS25 강남역점",
        "brand": "GS25",
        "lat": 37.4979,
        "lng": 127.0276,
        "address": "서울특별시 강남구 테헤란로 101 (강남역 11번 출구 앞)",
        "open24": True
    },
    {
        "id": "ST003",
        "name": "CU 홍대입구역점",
        "brand": "CU",
        "lat": 37.5563,
        "lng": 126.9226,
        "address": "서울특별시 마포구 양화로 160 (홍대입구역 9번 출구 앞)",
        "open24": True
    },
    {
        "id": "ST004",
        "name": "7-ELEVEN 서초중앙점",
        "brand": "7-ELEVEN",
        "lat": 37.4912,
        "lng": 127.0142,
        "address": "서울특별시 서초구 서초대로 250 (교대역 14번 출구)",
        "open24": False
    },
    {
        "id": "ST005",
        "name": "EMART24 명동플래그십점",
        "brand": "EMART24",
        "lat": 37.5635,
        "lng": 126.9850,
        "address": "서울특별시 중구 명동길 43 (명동 중심가)",
        "open24": True
    },
    {
        "id": "ST006",
        "name": "7-ELEVEN 역삼포스코점",
        "brand": "7-ELEVEN",
        "lat": 37.4965,
        "lng": 127.0260,
        "address": "서울특별시 강남구 역삼로 108 (역삼역 인근)",
        "open24": True
    },
    {
        "id": "ST007",
        "name": "GS25 서초중앙점",
        "brand": "GS25",
        "lat": 37.4930,
        "lng": 127.0160,
        "address": "서울특별시 서초구 반포대로 120 (서초역 3번 출구)",
        "open24": True
    },
    {
        "id": "ST008",
        "name": "CU 여의도역점",
        "brand": "CU",
        "lat": 37.5216,
        "lng": 126.9242,
        "address": "서울특별시 영등포구 여의나루로 42 (여의도역 5번 출구)",
        "open24": True
    },
    {
        "id": "ST009",
        "name": "GS25 잠실롯데타워점",
        "brand": "GS25",
        "lat": 37.5133,
        "lng": 127.1001,
        "address": "서울특별시 송파구 올림픽로 300 (잠실역 2번 출구)",
        "open24": True
    },
    {
        "id": "ST010",
        "name": "7-ELEVEN 종로3가역점",
        "brand": "7-ELEVEN",
        "lat": 37.5704,
        "lng": 126.9920,
        "address": "서울특별시 종로구 종로 115 (종로3가역 1번 출구)",
        "open24": True
    },
    {
        "id": "ST011",
        "name": "EMART24 광화문D타워점",
        "brand": "EMART24",
        "lat": 37.5709,
        "lng": 126.9789,
        "address": "서울특별시 종로구 종로3길 17 (광화문 D타워 1층)",
        "open24": True
    },
    {
        "id": "ST012",
        "name": "GS25 성수카페거리점",
        "brand": "GS25",
        "lat": 37.5445,
        "lng": 127.0560,
        "address": "서울특별시 성동구 연무장길 35 (성수역 3번 출구)",
        "open24": True
    },
    {
        "id": "ST013",
        "name": "CU 이태원역점",
        "brand": "CU",
        "lat": 37.5345,
        "lng": 126.9942,
        "address": "서울특별시 용산구 이태원로 179 (이태원역 1번 출구)",
        "open24": True
    },
    {
        "id": "ST014",
        "name": "GS25 해운대비치점",
        "brand": "GS25",
        "lat": 35.1587,
        "lng": 129.1604,
        "address": "부산광역시 해운대구 해운대해변로 264 (해운대 해수욕장 앞)",
        "open24": True
    },
    {
        "id": "ST015",
        "name": "7-ELEVEN 서면역점",
        "brand": "7-ELEVEN",
        "lat": 35.1578,
        "lng": 129.0592,
        "address": "부산광역시 부산진구 중앙대로 712 (서면역 7번 출구)",
        "open24": True
    },
    {
        "id": "ST016",
        "name": "GS25 동성로중앙점",
        "brand": "GS25",
        "lat": 35.8694,
        "lng": 128.5955,
        "address": "대구광역시 중구 동성로 25 (중앙로역 인근)",
        "open24": True
    },
    {
        "id": "ST017",
        "name": "CU 유성온천역점",
        "brand": "CU",
        "lat": 36.3537,
        "lng": 127.3415,
        "address": "대전광역시 유성구 대학로 84 (유성온천역 7번 출구)",
        "open24": True
    },
    {
        "id": "ST018",
        "name": "GS25 충장로점",
        "brand": "GS25",
        "lat": 35.1473,
        "lng": 126.9180,
        "address": "광주광역시 동구 충장로 46 (문화전당역 인근)",
        "open24": True
    },
    {
        "id": "ST019",
        "name": "CU 제주공항점",
        "brand": "CU",
        "lat": 33.5066,
        "lng": 126.4928,
        "address": "제주특별자치도 제주시 공항로 2 (제주국제공항 1층)",
        "open24": True
    },
    {
        "id": "ST020",
        "name": "EMART24 판교테크노점",
        "brand": "EMART24",
        "lat": 37.4020,
        "lng": 127.1086,
        "address": "경기도 성남시 분당구 판교역로 235 (판교테크노밸리)",
        "open24": True
    }
]

def fix_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    stores_clean = []

    for s in PRECISE_STORES_CLEAN:
        matching_prods = [
            {
                "product_id": p["id"],
                "product_name": p["name"],
                "event_type": p["event_type"],
                "price": p["price"],
                "unit_price": p["unit_price"],
                "is_in_stock": True,
                "last_pos_sync": "2026-08-01 00:00:00"
            }
            for p in products if p["brand"].upper() == s["brand"].upper()
        ]
        stores_clean.append({
            "id": s["id"],
            "name": s["name"],
            "brand": s["brand"],
            "lat": s["lat"],
            "lng": s["lng"],
            "address": s["address"],
            "open24": s["open24"],
            "inventory": matching_prods,
            "total_event_items": len(matching_prods)
        })

    data["stores"] = stores_clean
    data["metadata"]["total_stores"] = len(stores_clean)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(ROOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Cleaned cvs_data.json! Written {len(stores_clean)} 100% matched stores!")

if __name__ == "__main__":
    fix_data()
