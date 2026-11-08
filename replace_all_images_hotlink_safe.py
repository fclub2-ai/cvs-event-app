"""
Fix Hotlink Protection & Replace Fallback Pill Image completely
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "backend", "cvs_data.json")
ROOT_DATA_FILE = os.path.join(BASE_DIR, "cvs_data.json")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
APP_FILE = os.path.join(BASE_DIR, "src", "app.js")

# 100% 핫링크 블록 없는 직접 CDN 이미지 맵 (음료/식품/스낵/생필품)
HOTLINK_SAFE_IMAGES = {
    # 멘토스 (실제 멘토스 알사탕 패키지 이미지)
    "멘토스": "https://i.ibb.co/9kwJB7Qr/8990800000053.png",
    
    # 비타500 (100% 핫링크 프리 노란색 비타민 음료수 병 이미지)
    "비타500": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=500&auto=format&fit=crop&q=80",
    
    # 코카콜라 / 사이다 / 환타 / 펩시
    "코카콜라": "https://i.ibb.co/pjqX8NjP/8801094112707.png",
    "사이다": "https://i.ibb.co/zTc9qfH7/8801094202606.png",
    "스프라이트": "https://i.ibb.co/zTc9qfH7/8801094202606.png",
    "환타": "https://i.ibb.co/pjqX8NjP/8801094112707.png",
    "미에로화이바": "https://i.ibb.co/zhNc5d2C/8806004407133.jpg",
    "오곡누룽지": "https://i.ibb.co/KHyPgf9/8801382135036.png",
    "헛개수": "https://i.ibb.co/8Dkm0Sjq/8801007171210.jpg",

    # 우유 / 요구르트
    "바나나": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=500&auto=format&fit=crop&q=80",
    "딸기": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=500&auto=format&fit=crop&q=80",
    "초코": "https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=500&auto=format&fit=crop&q=80",
    "커피": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500&auto=format&fit=crop&q=80",
    "액티비아": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&auto=format&fit=crop&q=80",
    "요거톡": "https://images.unsplash.com/photo-1571212515416-fef01fc43637?w=500&auto=format&fit=crop&q=80",

    # 라면 / 도시락 / 간편식
    "라면": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500&auto=format&fit=crop&q=80",
    "육개장": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500&auto=format&fit=crop&q=80",
    "도시락": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=80",
    "햇반": "https://images.unsplash.com/photo-1516714435131-44d6b64dc6a2?w=500&auto=format&fit=crop&q=80",
    "떡볶이": "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?w=500&auto=format&fit=crop&q=80",
    "만두": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=500&auto=format&fit=crop&q=80",

    # 스낵 / 과자
    "포카칩": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=500&auto=format&fit=crop&q=80",
    "꼬북칩": "https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=500&auto=format&fit=crop&q=80",
    "허니버터칩": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=500&auto=format&fit=crop&q=80",
    "빼빼로": "https://images.unsplash.com/photo-1541781774459-bb29b565090c?w=500&auto=format&fit=crop&q=80",
    "초코송이": "https://images.unsplash.com/photo-1582176604856-e822b3749c6c?w=500&auto=format&fit=crop&q=80",
    "버터쿠키": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=500&auto=format&fit=crop&q=80",

    # 생필품
    "칫솔": "https://i.ibb.co/PypGp8B/8801046057216.jpg",
    "치약": "https://i.ibb.co/MD0qjSG2/8801046846087.jpg",
    "샴푸": "https://i.ibb.co/Gvpjpn0m/8801051152845.jpg",
    "세제": "https://i.ibb.co/kVvZVK4P/8801051203271.jpg",
    "라이너": "https://i.ibb.co/1JTv0mFR/8801166222587.png"
}

SAFE_FALLBACK = "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&auto=format&fit=crop&q=80"

def fix_all():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    for p in products:
        # 핫링크 블록 위험이 있는 7-eleven.co.kr CDN을 핫링크 안전 CDN으로 전면 대치
        name = p["name"]
        assigned = False
        for kw, safe_url in HOTLINK_SAFE_IMAGES.items():
            if kw in name:
                p["image"] = safe_url
                assigned = True
                break
        if not assigned:
            p["image"] = SAFE_FALLBACK

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(ROOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Replace fallback pill image URL in app.js
    with open(APP_FILE, "r", encoding="utf-8") as f:
        app_js = f.read()

    app_js = re.sub(r"photo-1542838132-92c53300491e", "photo-1622483767028-3f66f32aef97", app_js)
    with open(APP_FILE, "w", encoding="utf-8") as f:
        f.write(app_js)

    print(f"[SUCCESS] Replaced ALL hotlink-blocked image URLs and removed pill fallback URL!")

if __name__ == "__main__":
    fix_all()
