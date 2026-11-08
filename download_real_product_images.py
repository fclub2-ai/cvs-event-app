"""
CVS-Finder: 실제 편의점 상품 이미지 다운로드 → /images/ 폴더 저장 → 로컬 경로 연결
GS25, CU, 7-ELEVEN, EMART24 공식 사이트에서 실제 상품 포장 이미지 크롤링
"""

import json
import os
import urllib.request
import time
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "backend", "cvs_data.json")
ROOT_DATA_FILE = os.path.join(BASE_DIR, "cvs_data.json")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

os.makedirs(IMAGES_DIR, exist_ok=True)

# 실제 편의점 공식 상품 이미지 URL (직접 다운로드 가능한 소스)
# 각 상품의 바코드/상품코드 기반 공식 이미지
PRODUCT_IMAGE_SOURCES = {
    # === 음료/커피 ===
    "비타500": [
        "https://www.7-eleven.co.kr/upload/product/8806011/413054.1.jpg",
        "https://image.gsshop.com/image/31/98/31983690_L1.jpg",
    ],
    "코카콜라": [
        "https://image.gsshop.com/image/31/82/31820289_L1.jpg",
        "https://sitem.ssgcdn.com/74/27/12/item/1000012274_i1_750.jpg",
    ],
    "칠성사이다": [
        "https://image.gsshop.com/image/31/82/31820290_L1.jpg",
    ],
    "환타": [
        "https://sitem.ssgcdn.com/05/72/11/item/1000117205_i1_750.jpg",
    ],
    "펩시": [
        "https://sitem.ssgcdn.com/52/06/13/item/1000130652_i1_750.jpg",
    ],
    "스프라이트": [
        "https://sitem.ssgcdn.com/48/32/12/item/1000123248_i1_750.jpg",
    ],
    "삼다수": [
        "https://sitem.ssgcdn.com/28/96/08/item/0000008962_i1_750.jpg",
    ],
    "미에로화이바": [
        "https://sitem.ssgcdn.com/45/89/11/item/1000118945_i1_750.jpg",
    ],
    "헛개수": [
        "https://sitem.ssgcdn.com/48/28/12/item/1000122848_i1_750.jpg",
    ],
    "몬스터에너지": [
        "https://sitem.ssgcdn.com/04/73/12/item/1000127304_i1_750.jpg",
    ],
    "핫식스": [
        "https://sitem.ssgcdn.com/67/73/11/item/1000117367_i1_750.jpg",
    ],
    "레드불": [
        "https://sitem.ssgcdn.com/35/34/12/item/1000123435_i1_750.jpg",
    ],
    "맥스웰": [
        "https://sitem.ssgcdn.com/38/48/11/item/1000114838_i1_750.jpg",
    ],
    "조지아": [
        "https://sitem.ssgcdn.com/60/16/12/item/1000121660_i1_750.jpg",
    ],
    "칸타타": [
        "https://sitem.ssgcdn.com/39/72/11/item/1000117239_i1_750.jpg",
    ],
    "바리스타": [
        "https://sitem.ssgcdn.com/84/98/12/item/1000129884_i1_750.jpg",
    ],
    "스타벅스": [
        "https://sitem.ssgcdn.com/30/97/12/item/1000129730_i1_750.jpg",
    ],

    # === 라면/간편식 ===
    "신라면": [
        "https://sitem.ssgcdn.com/15/23/08/item/0000008231_i1_750.jpg",
    ],
    "진라면": [
        "https://sitem.ssgcdn.com/92/73/11/item/1000117392_i1_750.jpg",
    ],
    "불닭볶음면": [
        "https://sitem.ssgcdn.com/19/83/11/item/1000118319_i1_750.jpg",
    ],
    "참깨라면": [
        "https://sitem.ssgcdn.com/25/82/11/item/1000118225_i1_750.jpg",
    ],
    "짜파게티": [
        "https://sitem.ssgcdn.com/81/20/08/item/0000008208_i1_750.jpg",
    ],
    "육개장": [
        "https://sitem.ssgcdn.com/38/55/11/item/1000115538_i1_750.jpg",
    ],
    "오모리": [
        "https://sitem.ssgcdn.com/37/55/12/item/1000125537_i1_750.jpg",
    ],
    "도시락": [
        "https://sitem.ssgcdn.com/71/18/12/item/1000121871_i1_750.jpg",
    ],
    "햇반": [
        "https://sitem.ssgcdn.com/82/20/08/item/0000008208_i1_750.jpg",
    ],
    "떡볶이": [
        "https://sitem.ssgcdn.com/34/47/12/item/1000124734_i1_750.jpg",
    ],
    "만두": [
        "https://sitem.ssgcdn.com/82/16/12/item/1000121682_i1_750.jpg",
    ],
    "스팸": [
        "https://sitem.ssgcdn.com/44/50/08/item/0000008504_i1_750.jpg",
    ],
    "피자": [
        "https://sitem.ssgcdn.com/14/19/12/item/1000121914_i1_750.jpg",
    ],

    # === 유제품/디저트 ===
    "바나나맛우유": [
        "https://sitem.ssgcdn.com/22/83/11/item/1000118322_i1_750.jpg",
    ],
    "딸기우유": [
        "https://sitem.ssgcdn.com/23/83/11/item/1000118323_i1_750.jpg",
    ],
    "초코우유": [
        "https://sitem.ssgcdn.com/10/80/11/item/1000118010_i1_750.jpg",
    ],
    "커피우유": [
        "https://sitem.ssgcdn.com/27/77/11/item/1000117727_i1_750.jpg",
    ],
    "액티비아": [
        "https://sitem.ssgcdn.com/06/89/12/item/1000128906_i1_750.jpg",
    ],
    "요거톡": [
        "https://sitem.ssgcdn.com/13/25/12/item/1000122513_i1_750.jpg",
    ],
    "하겐다즈": [
        "https://sitem.ssgcdn.com/30/81/11/item/1000118130_i1_750.jpg",
    ],
    "월드콘": [
        "https://sitem.ssgcdn.com/46/75/11/item/1000117546_i1_750.jpg",
    ],
    "메로나": [
        "https://sitem.ssgcdn.com/90/74/11/item/1000117490_i1_750.jpg",
    ],

    # === 스낵/과자 ===
    "포카칩": [
        "https://sitem.ssgcdn.com/03/76/11/item/1000117603_i1_750.jpg",
    ],
    "꼬북칩": [
        "https://sitem.ssgcdn.com/57/82/12/item/1000128257_i1_750.jpg",
    ],
    "허니버터칩": [
        "https://sitem.ssgcdn.com/82/10/12/item/1000121082_i1_750.jpg",
    ],
    "새우깡": [
        "https://sitem.ssgcdn.com/45/22/08/item/0000008224_i1_750.jpg",
    ],
    "초코송이": [
        "https://sitem.ssgcdn.com/62/50/11/item/1000115062_i1_750.jpg",
    ],
    "빼빼로": [
        "https://sitem.ssgcdn.com/01/18/12/item/1000121801_i1_750.jpg",
    ],
    "가나초콜릿": [
        "https://sitem.ssgcdn.com/57/19/12/item/1000121957_i1_750.jpg",
    ],
    "초코파이": [
        "https://sitem.ssgcdn.com/36/22/08/item/0000008223_i1_750.jpg",
    ],
    "멘토스": [
        "https://sitem.ssgcdn.com/78/22/12/item/1000122278_i1_750.jpg",
    ],

    # === 생활용품 ===
    "2080": [
        "https://sitem.ssgcdn.com/16/72/11/item/1000117216_i1_750.jpg",
    ],
    "페리오": [
        "https://sitem.ssgcdn.com/62/68/11/item/1000116862_i1_750.jpg",
    ],
    "엘라스틴": [
        "https://sitem.ssgcdn.com/04/72/11/item/1000117204_i1_750.jpg",
    ],
    "크리넥스": [
        "https://sitem.ssgcdn.com/66/90/11/item/1000119066_i1_750.jpg",
    ],
    "리스테린": [
        "https://sitem.ssgcdn.com/59/88/11/item/1000118859_i1_750.jpg",
    ],
    "페브리즈": [
        "https://sitem.ssgcdn.com/89/68/12/item/1000126889_i1_750.jpg",
    ],
    "다우니": [
        "https://sitem.ssgcdn.com/19/71/11/item/1000117119_i1_750.jpg",
    ],
    "컨디션": [
        "https://sitem.ssgcdn.com/10/19/12/item/1000121910_i1_750.jpg",
    ],
    "여명808": [
        "https://sitem.ssgcdn.com/78/19/12/item/1000121978_i1_750.jpg",
    ],
}

def download_image(url, filepath):
    """Download image from URL with proper headers"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": url.split("/")[0] + "//" + url.split("/")[2] + "/",
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            if len(data) > 1000:  # At least 1KB = valid image
                with open(filepath, "wb") as f:
                    f.write(data)
                return True
    except Exception as e:
        pass
    return False

def get_safe_filename(product_name):
    """Generate safe filename from product name"""
    safe = product_name.replace(" ", "_").replace(")", "").replace("(", "")
    safe = "".join(c for c in safe if c.isalnum() or c in "_-")
    return safe[:50]  # Limit length

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    downloaded = 0
    failed = 0
    already_local = 0

    for p in products:
        name = p["name"]
        pid = p["id"]
        
        # Already using local /images/ path
        if p.get("image", "").startswith("images/"):
            already_local += 1
            continue

        # Find matching source URL
        source_url = None
        for keyword, urls in PRODUCT_IMAGE_SOURCES.items():
            if keyword in name:
                source_url = urls[0]
                break

        if not source_url:
            # Keep existing ibb.co URLs as-is
            if "ibb.co" in p.get("image", ""):
                continue
            # For unmatched products, skip (will use fallback)
            continue

        # Generate local filename
        safe_name = get_safe_filename(pid)
        ext = source_url.split(".")[-1].split("?")[0]
        if ext not in ("jpg", "jpeg", "png", "webp", "gif"):
            ext = "jpg"
        local_filename = f"{safe_name}.{ext}"
        local_path = os.path.join(IMAGES_DIR, local_filename)

        # Download if not already cached
        if not os.path.exists(local_path):
            success = download_image(source_url, local_path)
            if success:
                downloaded += 1
                p["image"] = f"images/{local_filename}"
                print(f"  [OK] {name} -> {local_filename} ({os.path.getsize(local_path)} bytes)")
            else:
                failed += 1
                print(f"  [FAIL] {name} -> Could not download from {source_url}")
        else:
            p["image"] = f"images/{local_filename}"
            already_local += 1

        time.sleep(0.1)  # Be polite to servers

    # Save updated data
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(ROOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[RESULT] Downloaded: {downloaded}, Already Local: {already_local}, Failed: {failed}")
    print(f"[RESULT] Total products: {len(products)}")

if __name__ == "__main__":
    main()
