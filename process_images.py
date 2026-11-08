import os
import json
import urllib.request
import urllib.parse
import re
import base64
import ssl

# Target 21 items with keywords to match in cvs_data.json
TARGET_ITEMS = [
    {"name": "나뚜루 파인트 녹차 474ml", "keywords": ["나뚜루", "녹차"]},
    {"name": "롯데 월드콘 바닐라 160ml", "keywords": ["월드콘", "바닐라"]},
    {"name": "빙그레 메로나 70ml", "keywords": ["메로나"]},
    {"name": "오리온 포카칩 오리지널 66g", "keywords": ["포카칩", "오리지널"]},
    {"name": "오리온 꼬북칩 콘스프맛 80g", "keywords": ["꼬북칩", "콘스프"]},
    {"name": "해태 허니버터칩 60g", "keywords": ["허니버터칩"]},
    {"name": "농심 새우깡 90g", "keywords": ["새우깡"]},
    {"name": "오리온 초코송이 50g", "keywords": ["초코송이"]},
    {"name": "롯데 빼빼로 아몬드 37g", "keywords": ["빼빼로", "아몬드"]},
    {"name": "롯데 가나 딥밀크 초콜릿 70g", "keywords": ["가나", "딥밀크"]},
    {"name": "페레로로쉐 T3 37.5g", "keywords": ["페레로", "T3"]},
    {"name": "하리보 골드베렌 곰젤리 100g", "keywords": ["하리보", "골드베렌"]},
    {"name": "오리온 초코파이 12입 팩", "keywords": ["초코파이"]},
    {"name": "롯데 칙촉 120g", "keywords": ["칙촉"]},
    {"name": "크리넥스 수프림소프트 30롤", "keywords": ["크리넥스", "수프림소프트"]},
    {"name": "리스테린 쿨민트 구강청결제 750ml", "keywords": ["리스테린", "쿨민트"]},
    {"name": "가그린 제로 구강청결제 750ml", "keywords": ["가그린", "제로"]},
    {"name": "페브리즈 깨끗한향 370ml", "keywords": ["페브리즈", "깨끗한향"]},
    {"name": "다우니 아로마보라 섬유유연제 1L", "keywords": ["다우니", "아로마보라"]},
    {"name": "컨디션 스틱 헛개 18g", "keywords": ["컨디션", "스틱"]},
    {"name": "여명808 숙취해소음료 140ml", "keywords": ["여명808"]}
]

DATA_FILES = [
    r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json",
    r"C:\Users\fclub\cvs-event-app\cvs_data.json"
]

IMGBB_API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

def main():
    print("Checking JSON data files...")
    for path in DATA_FILES:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"{path}: total products {len(data.get('products', []))}")
            
            # Find matches for each target item
            for item in TARGET_ITEMS:
                matches = []
                for p in data.get('products', []):
                    p_name = p.get('name', '')
                    if all(kw in p_name for kw in item['keywords']):
                        matches.append((p.get('id'), p_name, p.get('brand'), p.get('image')))
                print(f"Target: {item['name']} -> Found {len(matches)} matches")
                for m in matches:
                    print(f"  [{m[2]}] {m[1]} ({m[0]}) -> Current Image: {m[3]}")

if __name__ == "__main__":
    main()
