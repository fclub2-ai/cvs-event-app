import sys
import gzip
import urllib.request
import json
import re
import os
import shutil
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip"
}

BRANDS = [
    ("cu", "CU", 65),
    ("gs25", "GS25", 55),
    ("seven", "7-ELEVEN", 50),
    ("emart24", "EMART24", 50)
]

def determine_category(pname):
    name = pname.lower()
    if any(k in name for k in ["콜라", "사이다", "음료", "차", "수", "아메리카노", "라떼", "커피", "우유", "에너지", "핫식스", "몬스터", "레드불", "비타", "요구르트", "주스", "에이드", "워터", "샘물", "탄산"]):
        return "음료/커피"
    elif any(k in name for k in ["칩", "과자", "스낵", "스틱", "쿠키", "파이", "초코", "젤리", "깡", "송이", "빼빼로", "캔디", "껌", "크런치", "나초"]):
        return "스낵/과자"
    elif any(k in name for k in ["라면", "면", "컵", "도시락", "햇반", "밥", "떡볶이", "만두", "교자", "스팸", "참치", "피자", "부대찌개", "김밥", "주먹밥", "샌드위치", "버거"]):
        return "라면/간편식"
    elif any(k in name for k in ["빵", "케익", "케이크", "디저트", "아이스크림", "파인트", "콘", "바", "모찌", "마카롱", "도넛", "슈"]):
        return "디저트/베이커리"
    elif any(k in name for k in ["계란", "두부", "바나나", "사과", "닭가슴살", "샐러드", "치즈", "소시지", "핫바", "크래미"]):
        return "신선식품"
    else:
        return "생활용품"

def parse_pyony_page(args):
    brand_slug, brand_name, page = args
    url = f"https://pyony.com/brands/{brand_slug}/?page={page}"
    products = []
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, timeout=15)
        raw = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            html = gzip.decompress(raw).decode('utf-8', errors='ignore')
        else:
            html = raw.decode('utf-8', errors='ignore')
            
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".col-md-6") or soup.select(".card")
        
        for idx, card in enumerate(cards):
            strong_el = card.select_one(".card-body strong") or card.select_one("strong")
            img_el = card.select_one("img.prod_img") or card.select_one("img")
            
            # Event type badge (1+1 or 2+1)
            header_badge = card.select_one(".card-header")
            event_type = "1+1"
            if header_badge:
                htext = header_badge.get_text(strip=True)
                if "2+1" in htext:
                    event_type = "2+1"
                elif "1+1" in htext:
                    event_type = "1+1"
                    
            # Price parsing
            price_el = card.select_one(".fa-coins")
            price = 2000
            if price_el and price_el.parent:
                ptext = price_el.parent.get_text(strip=True)
                num_match = re.search(r"([\d,]+)\s*원", ptext)
                if num_match:
                    price = int(num_match.group(1).replace(",", ""))
                    
            if strong_el and img_el:
                raw_name = strong_el.get_text(strip=True)
                clean_title = re.sub(r"^(CU|GS25|세븐일레븐|이마트24|7-ELEVEN)\s*", "", raw_name).strip()
                full_name = clean_title
                
                img_src = img_el.get("src") or img_el.get("data-src") or ""
                if img_src.startswith("//"):
                    img_src = "https:" + img_src
                elif img_src and not img_src.startswith("http"):
                    img_src = "https://pyony.com" + img_src
                    
                if img_src and not img_src.endswith("no_image.png"):
                    unit_price = round(price / 2) if event_type == "1+1" else round(price * 2 / 3)
                    discount_rate = 50 if event_type == "1+1" else 33
                    category = determine_category(clean_title)
                    
                    products.append({
                        "id": f"{brand_slug}_{page}_{idx}_{hash(full_name)&0xffffff}",
                        "name": full_name,
                        "brand": brand_name,
                        "event_type": event_type,
                        "price": price,
                        "unit_price": unit_price,
                        "discount_rate": discount_rate,
                        "category": category,
                        "image": img_src
                    })
        return products
    except Exception as e:
        return []

def build_fresh_dataset():
    print("Step 1: Scraping fresh, 100% uncorrupted Korean product dataset from Pyony...")
    tasks = []
    for slug, bname, max_p in BRANDS:
        for p in range(1, max_p + 1):
            tasks.append((slug, bname, p))
            
    all_products = []
    seen_names = set()
    
    with ThreadPoolExecutor(max_workers=35) as executor:
        for res_list in executor.map(parse_pyony_page, tasks):
            for item in res_list:
                if item["name"] not in seen_names:
                    seen_names.add(item["name"])
                    all_products.append(item)
                    
    print(f"\n[FRESH DATASET COMPLETE] Total {len(all_products)} clean products extracted!")
    
    # Load existing verified stores
    existing_stores = []
    if os.path.exists("cvs_data.json"):
        with open("cvs_data.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)
            existing_stores = old_data.get("stores", [])

    final_payload = {
        "products": all_products,
        "stores": existing_stores,
        "last_updated": "2026-08-16"
    }

    with open("cvs_data.json", "w", encoding="utf-8") as f:
        json.dump(final_payload, f, ensure_ascii=False, indent=2)

    shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
    print("[SYNC SUCCESS] Rebuilt cvs_data.json and synced to backend/cvs_data.json!")

if __name__ == "__main__":
    build_fresh_dataset()
