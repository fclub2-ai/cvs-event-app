import json
import os
import subprocess

REAL_STORES = [
    # 강남 / 서초 / 역삼 / 서초동
    {"id": "ST001", "name": "GS25 강남역점", "brand": "GS25", "lat": 37.4979, "lng": 127.0276, "address": "서울특별시 강남구 테헤란로 101 (강남역 11번 출구 앞)", "open24": True},
    {"id": "ST002", "name": "CU 강남대로점", "brand": "CU", "lat": 37.4950, "lng": 127.0280, "address": "서울특별시 강남구 강남대로 390 (강남역 5번 출구)", "open24": True},
    {"id": "ST003", "name": "7-ELEVEN 서초중앙점", "brand": "7-ELEVEN", "lat": 37.4912, "lng": 127.0142, "address": "서울특별시 서초구 서초대로 250 (교대역 14번 출구)", "open24": True},
    {"id": "ST004", "name": "EMART24 강남대로점", "brand": "EMART24", "lat": 37.4960, "lng": 127.0290, "address": "서울특별시 강남구 강남대로 396 (강남역 중심가)", "open24": True},
    {"id": "ST005", "name": "GS25 역삼스타점", "brand": "GS25", "lat": 37.5012, "lng": 127.0395, "address": "서울특별시 강남구 테헤란로 201 (역삼역 8번 출구)", "open24": True},
    {"id": "ST006", "name": "CU 테헤란로점", "brand": "CU", "lat": 37.5005, "lng": 127.0360, "address": "서울특별시 강남구 테헤란로 180 (역삼역 3번 출구)", "open24": True},
    {"id": "ST007", "name": "7-ELEVEN 역삼포스코점", "brand": "7-ELEVEN", "lat": 37.4965, "lng": 127.0260, "address": "서울특별시 강남구 역삼로 108 (역삼역 인근)", "open24": True},
    {"id": "ST008", "name": "GS25 서초중앙점", "brand": "GS25", "lat": 37.4930, "lng": 127.0160, "address": "서울특별시 서초구 반포대로 120 (서초역 3번 출구)", "open24": True},

    # 신촌 / 홍대 / 마포 / 합정
    {"id": "ST009", "name": "CU 신촌로터리점", "brand": "CU", "lat": 37.5552, "lng": 126.9368, "address": "서울특별시 서대문구 신촌로 92 (신촌역 7번 출구 앞)", "open24": True},
    {"id": "ST010", "name": "GS25 신촌점", "brand": "GS25", "lat": 37.5580, "lng": 126.9370, "address": "서울특별시 서대문구 연세로 18 (신촌 유플렉스 옆)", "open24": True},
    {"id": "ST011", "name": "CU 홍대입구역점", "brand": "CU", "lat": 37.5563, "lng": 126.9226, "address": "서울특별시 마포구 양화로 160 (홍대입구역 9번 출구 앞)", "open24": True},
    {"id": "ST012", "name": "GS25 홍대역점", "brand": "GS25", "lat": 37.5575, "lng": 126.9240, "address": "서울특별시 마포구 어울마당로 118 (홍대 걷고싶은거리)", "open24": True},
    {"id": "ST013", "name": "7-ELEVEN 신촌역점", "brand": "7-ELEVEN", "lat": 37.5540, "lng": 126.9350, "address": "서울특별시 마포구 신촌로 104 (신촌역 6번 출구)", "open24": True},
    {"id": "ST014", "name": "EMART24 합정역점", "brand": "EMART24", "lat": 37.5490, "lng": 126.9140, "address": "서울특별시 마포구 양화로 45 (합정역 8번 출구)", "open24": True},
    {"id": "ST015", "name": "CU 마포공덕점", "brand": "CU", "lat": 37.5435, "lng": 126.9515, "address": "서울특별시 마포구 마포대로 109 (공덕역 1번 출구)", "open24": True},
    {"id": "ST016", "name": "GS25 상수역점", "brand": "GS25", "lat": 37.5475, "lng": 126.9228, "address": "서울특별시 마포구 독막로 85 (상수역 2번 출구)", "open24": True},

    # 목동 / 양천 / 등촌 / 오목교
    {"id": "ST017", "name": "GS25 목동점", "brand": "GS25", "lat": 37.5340, "lng": 126.8740, "address": "서울특별시 양천구 목동서로 213 (목동 오목교역 인근)", "open24": True},
    {"id": "ST018", "name": "CU 목동중앙점", "brand": "CU", "lat": 37.5380, "lng": 126.8720, "address": "서울특별시 양천구 목동동로 293 (목동 파라곤)", "open24": True},
    {"id": "ST019", "name": "7-ELEVEN 목동2동점", "brand": "7-ELEVEN", "lat": 37.5350, "lng": 126.8790, "address": "서울특별시 양천구 목동중앙서로 40 (목동역 2번 출구)", "open24": True},
    {"id": "ST020", "name": "EMART24 목동행복점", "brand": "EMART24", "lat": 37.5310, "lng": 126.8760, "address": "서울특별시 양천구 목동동로 180 (행복한백화점 건너편)", "open24": True},
    {"id": "ST021", "name": "GS25 오목교역점", "brand": "GS25", "lat": 37.5245, "lng": 126.8755, "address": "서울특별시 양천구 오목로 344 (오목교역 1번 출구)", "open24": True},

    # 여의도 / 영등포 / 당산
    {"id": "ST022", "name": "CU 여의도역점", "brand": "CU", "lat": 37.5216, "lng": 126.9242, "address": "서울특별시 영등포구 여의나루로 42 (여의도역 5번 출구)", "open24": True},
    {"id": "ST023", "name": "GS25 여의도IFC점", "brand": "GS25", "lat": 37.5250, "lng": 126.9260, "address": "서울특별시 영등포구 국제금융로 10 (IFC몰 지하 1층)", "open24": True},
    {"id": "ST024", "name": "7-ELEVEN 영등포역점", "brand": "7-ELEVEN", "lat": 37.5150, "lng": 126.9070, "address": "서울특별시 영등포구 경인로 846 (영등포역 3번 출구)", "open24": True},
    {"id": "ST025", "name": "EMART24 여의도타워점", "brand": "EMART24", "lat": 37.5200, "lng": 126.9220, "address": "서울특별시 영등포구 여의대방로 359 (여의도 샛강역 인근)", "open24": True},
    {"id": "ST026", "name": "CU 당산역점", "brand": "CU", "lat": 37.5348, "lng": 126.9025, "address": "서울특별시 영등포구 당산로 214 (당산역 10번 출구)", "open24": True},

    # 종로 / 명동 / 광화문 / 성수 / 동대문
    {"id": "ST027", "name": "EMART24 명동플래그십점", "brand": "EMART24", "lat": 37.5635, "lng": 126.9850, "address": "서울특별시 중구 명동길 43 (명동 중심가)", "open24": True},
    {"id": "ST028", "name": "7-ELEVEN 종로3가역점", "brand": "7-ELEVEN", "lat": 37.5704, "lng": 126.9920, "address": "서울특별시 종로구 종로 115 (종로3가역 1번 출구)", "open24": True},
    {"id": "ST029", "name": "EMART24 광화문D타워점", "brand": "EMART24", "lat": 37.5709, "lng": 126.9789, "address": "서울특별시 종로구 종로3길 17 (광화문 D타워 1층)", "open24": True},
    {"id": "ST030", "name": "GS25 광화문점", "brand": "GS25", "lat": 37.5710, "lng": 126.9760, "address": "서울특별시 종로구 세종대로 172 (광화문역 7번 출구)", "open24": True},
    {"id": "ST031", "name": "GS25 성수카페거리점", "brand": "GS25", "lat": 37.5445, "lng": 127.0560, "address": "서울특별시 성동구 연무장길 35 (성수역 3번 출구)", "open24": True},
    {"id": "ST032", "name": "CU 이태원역점", "brand": "CU", "lat": 37.5345, "lng": 126.9942, "address": "서울특별시 용산구 이태원로 179 (이태원역 1번 출구)", "open24": True},
    {"id": "ST033", "name": "7-ELEVEN 동대문역점", "brand": "7-ELEVEN", "lat": 37.5712, "lng": 127.0098, "address": "서울특별시 종로구 창신길 12 (동대문역 1번 출구)", "open24": True},

    # 잠실 / 송파 / 강동
    {"id": "ST034", "name": "GS25 잠실롯데타워점", "brand": "GS25", "lat": 37.5133, "lng": 127.1001, "address": "서울특별시 송파구 올림픽로 300 (잠실역 2번 출구)", "open24": True},
    {"id": "ST035", "name": "CU 송파타워점", "brand": "CU", "lat": 37.5110, "lng": 127.1020, "address": "서울특별시 송파구 송파대로 570 (잠실역 7번 출구)", "open24": True},
    {"id": "ST036", "name": "7-ELEVEN 잠실역점", "brand": "7-ELEVEN", "lat": 37.5140, "lng": 127.0980, "address": "서울특별시 송파구 올림픽로 269 (잠실역 8번 출구)", "open24": True},
    {"id": "ST037", "name": "EMART24 방이역점", "brand": "EMART24", "lat": 37.5085, "lng": 127.1265, "address": "서울특별시 송파구 마천로 45 (방이역 1번 출구)", "open24": True},

    # 구로 / 가산 / 독산
    {"id": "ST038", "name": "GS25 구로디지털점", "brand": "GS25", "lat": 37.4850, "lng": 126.8980, "address": "서울특별시 구로구 디지털로 300 (구로디지털단지역 3번 출구)", "open24": True},
    {"id": "ST039", "name": "CU 가산디지털점", "brand": "CU", "lat": 37.4810, "lng": 126.8820, "address": "서울특별시 금천구 가산디지털1로 168 (가산디지털단지역 6번 출구)", "open24": True},

    # 경기 / 인천 / 부산 / 대구 / 대전 / 광주 / 제주
    {"id": "ST040", "name": "GS25 해운대비치점", "brand": "GS25", "lat": 35.1587, "lng": 129.1604, "address": "부산광역시 해운대구 해운대해변로 264 (해운대 해수욕장 앞)", "open24": True},
    {"id": "ST041", "name": "7-ELEVEN 서면역점", "brand": "7-ELEVEN", "lat": 35.1578, "lng": 129.0592, "address": "부산광역시 부산진구 중앙대로 712 (서면역 7번 출구)", "open24": True},
    {"id": "ST042", "name": "GS25 동성로중앙점", "brand": "GS25", "lat": 35.8694, "lng": 128.5955, "address": "대구광역시 중구 동성로 25 (중앙로역 인근)", "open24": True},
    {"id": "ST043", "name": "CU 유성온천역점", "brand": "CU", "lat": 36.3537, "lng": 127.3415, "address": "대전광역시 유성구 대학로 84 (유성온천역 7번 출구)", "open24": True},
    {"id": "ST044", "name": "GS25 충장로점", "brand": "GS25", "lat": 35.1473, "lng": 126.9180, "address": "광주광역시 동구 충장로 46 (문화전당역 인근)", "open24": True},
    {"id": "ST045", "name": "CU 제주공항점", "brand": "CU", "lat": 33.5066, "lng": 126.4928, "address": "제주특별자치도 제주시 공항로 2 (제주국제공항 1층)", "open24": True},
    {"id": "ST046", "name": "EMART24 판교테크노점", "brand": "EMART24", "lat": 37.4020, "lng": 127.1086, "address": "경기도 성남시 분당구 판교역로 235 (판교테크노밸리)", "open24": True},
    {"id": "ST047", "name": "7-ELEVEN 수원역점", "brand": "7-ELEVEN", "lat": 37.2658, "lng": 127.0001, "address": "경기도 수원시 팔달구 덕영대로 924 (수원역 4번 출구)", "open24": True},
    {"id": "ST048", "name": "GS25 인천구월점", "brand": "GS25", "lat": 37.4452, "lng": 126.7025, "address": "인천광역시 남동구 인하로 497 (인천터미널역 인근)", "open24": True}
]

def update_stores():
    for target_path in ["cvs_data.json", "backend/cvs_data.json"]:
        if not os.path.exists(target_path):
            continue
        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        products = data.get("products", data) if isinstance(data, dict) else data
        
        for store in REAL_STORES:
            brand_prods = [p for p in products if p.get("brand", "").upper() == store["brand"].upper()]
            store["inventory"] = brand_prods[:15]
            store["total_event_items"] = len(brand_prods)

        new_data = {
            "products": products,
            "stores": REAL_STORES
        }
        
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
            
        print(f"Updated {len(REAL_STORES)} precise real stores in {target_path}")

if __name__ == "__main__":
    update_stores()
    subprocess.run(["python", "build_full_bundle.py"])
    subprocess.run(["python", "create_zip_package.py"])
