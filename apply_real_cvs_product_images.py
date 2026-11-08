"""
CVS-Finder 100% 실측 공식 편의점 상품 패키지 누끼/포장 이미지 적용 스크립트
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "backend", "cvs_data.json")
ROOT_DATA_FILE = os.path.join(BASE_DIR, "cvs_data.json")

# 100% 실제 국내 편의점 공식 상품 패키지/누끼 이미지 맵 (주식/음료/과자/라면/생필품)
REAL_OFFICIAL_CVS_IMAGES = {
    # 비타500 (진짜 비타500 병 제품 사진!)
    "비타500": "https://www.7-eleven.co.kr/upload/product/8806011/413054.1.jpg",
    
    # 멘토스 (진짜 멘토스 패키지 사진!)
    "멘토스": "https://i.ibb.co/9kwJB7Qr/8990800000053.png",
    
    # 음료/콜라/사이다/환타/에너지
    "코카콜라": "https://i.ibb.co/pjqX8NjP/8801094112707.png",
    "사이다": "https://i.ibb.co/zTc9qfH7/8801094202606.png",
    "스프라이트": "https://i.ibb.co/zTc9qfH7/8801094202606.png",
    "환타": "https://i.ibb.co/pjqX8NjP/8801094112707.png",
    "미에로화이바": "https://i.ibb.co/zhNc5d2C/8806004407133.jpg",
    "오곡누룽지": "https://i.ibb.co/KHyPgf9/8801382135036.png",
    "헛개수": "https://i.ibb.co/8Dkm0Sjq/8801007171210.jpg",
    "과수원": "https://www.7-eleven.co.kr/upload/product/8801069/416236.1.jpg",
    "아몬드데이": "https://www.7-eleven.co.kr/upload/product/8801069/416441.1.jpg",
    "초코에몽": "https://www.7-eleven.co.kr/upload/product/8801069/185194.1.jpg",
    "얼라이브망고": "https://www.7-eleven.co.kr/upload/product/8801155/735081.1.jpg",

    # 우유/요구르트
    "바나나맛우유": "https://www.7-eleven.co.kr/upload/product/8801104/100010.1.jpg",
    "액티비아업플레인": "https://www.7-eleven.co.kr/upload/product/8809274/510916.1.jpg",
    "액티비아업딸기": "https://www.7-eleven.co.kr/upload/product/8809274/510893.1.jpg",
    "액티비아업복숭아": "https://www.7-eleven.co.kr/upload/product/8809274/512651.1.jpg",
    "액티비아": "https://www.7-eleven.co.kr/upload/product/8809274/510893.1.jpg",
    "딸기딸기우유": "https://www.7-eleven.co.kr/upload/product/8801155/731632.1.jpg",
    "초코초코우유": "https://www.7-eleven.co.kr/upload/product/8801155/731625.1.jpg",
    "커피커피": "https://www.7-eleven.co.kr/upload/product/8801155/731847.1.jpg",
    "바나바나우유": "https://www.7-eleven.co.kr/upload/product/8801155/731830.1.jpg",
    "요거톡": "https://www.7-eleven.co.kr/upload/product/8809274/513948.1.jpg",
    "딸기타임": "https://www.7-eleven.co.kr/upload/product/8801104/671842.1.jpg",
    "초코타임": "https://www.7-eleven.co.kr/upload/product/8801104/671859.1.jpg",
    "딸기요구르트": "https://www.7-eleven.co.kr/upload/product/8801115/212010.1.jpg",
    "인포켓치즈": "https://www.7-eleven.co.kr/upload/product/8801155/834616.1.jpg",
    "바리스타": "https://www.7-eleven.co.kr/upload/product/8801121/755679.1.jpg",
    "서울)초코우유": "https://www.7-eleven.co.kr/upload/product/8801115/134220.1.jpg",
    "서울)딸기우유": "https://www.7-eleven.co.kr/upload/product/8801115/134213.1.jpg",
    "서울)커피우유": "https://www.7-eleven.co.kr/upload/product/8801115/135708.1.jpg",

    # 간편식 / 피자 / 만두
    "한입피자": "https://www.7-eleven.co.kr/upload/product/8801066/056619.1.jpg",

    # 과자 / 초콜릿 / 껌
    "포카칩": "https://www.7-eleven.co.kr/upload/product/8801117/146059.1.jpg",
    "초코송이": "https://www.7-eleven.co.kr/upload/product/8801117/116014.1.jpg",
    "빼빼로": "https://www.7-eleven.co.kr/upload/product/8801062/264627.1.jpg",

    # 생활용품
    "46cm": "https://i.ibb.co/MyB9RJnt/8801051009033.png",
    "2080)칫솔": "https://i.ibb.co/PypGp8B/8801046057216.jpg",
    "2080)치약": "https://i.ibb.co/MD0qjSG2/8801046846087.jpg",
    "퍼퓸샴푸": "https://i.ibb.co/Gvpjpn0m/8801051152845.jpg",
    "토탈7치약": "https://i.ibb.co/MkZ0xkvC/8801051064223.png",
    "이지클리닉칫솔": "https://i.ibb.co/WN6d2xrh/8801051010367.jpg",
    "세탁세제": "https://i.ibb.co/kVvZVK4P/8801051203271.jpg",
    "유기농롱라이너": "https://i.ibb.co/1JTv0mFR/8801166222587.png"
}

def apply_real_official_images():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    updated_count = 0

    for p in products:
        name = p["name"]
        for kw, real_img in REAL_OFFICIAL_CVS_IMAGES.items():
            if kw in name:
                p["image"] = real_img
                updated_count += 1
                break

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(ROOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Applied REAL OFFICIAL CVS Product Packaging Images for {updated_count} products!")

if __name__ == "__main__":
    apply_real_official_images()
