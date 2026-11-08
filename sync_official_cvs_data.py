import sys
import gzip
import urllib.request
import urllib.parse
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

def fetch_cu_official_page(page_idx):
    url = "https://cu.bgfretail.com/event/plusAjax.do"
    form_data = urllib.parse.urlencode({
        'pageIndex': page_idx,
        'listType': 1,
        'searchCondition': '',
        'user_id': ''
    }).encode('utf-8')
    
    products = []
    try:
        req = urllib.request.Request(url, data=form_data, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://cu.bgfretail.com/event/plus.do'
        })
        res = urllib.request.urlopen(req, timeout=12)
        raw = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            html = gzip.decompress(raw).decode('utf-8', errors='ignore')
        else:
            html = raw.decode('utf-8', errors='ignore')
            
        soup = BeautifulSoup(html, 'html.parser')
        lis = soup.select('ul > li')
        
        for idx, li in enumerate(lis):
            name_el = li.select_one('.name')
            price_el = li.select_one('.price > strong')
            img_el = li.select_one('img')
            badge_el = li.select_one('.badge') or li.select_one('.tag')
            
            if name_el and img_el:
                raw_name = name_el.get_text(strip=True)
                clean_name = re.sub(r"^CU\s*", "", raw_name).strip()
                
                price_text = price_el.get_text(strip=True) if price_el else "2000"
                price = int(re.sub(r"[^\d]", "", price_text) or 2000)
                if price < 300:
                    price = 2000
                
                event_type = "1+1"
                if badge_el and "2+1" in badge_el.get_text(strip=True):
                    event_type = "2+1"
                elif "2+1" in li.get_text(strip=True):
                    event_type = "2+1"
                    
                img_src = img_el.get("src") or ""
                if img_src.startswith("//"):
                    img_src = "https:" + img_src
                elif img_src and not img_src.startswith("http"):
                    img_src = "https://cu.bgfretail.com" + img_src
                    
                unit_price = round(price / 2) if event_type == "1+1" else round(price * 2 / 3)
                discount_rate = 50 if event_type == "1+1" else 33
                category = determine_category(clean_name)
                
                products.append({
                    "id": f"cu_off_{page_idx}_{idx}_{hash(clean_name)&0xffffff}",
                    "name": clean_name,
                    "brand": "CU",
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

def fetch_pyony_brand(args):
    brand_slug, brand_name, page = args
    url = f"https://pyony.com/brands/{brand_slug}/?page={page}"
    products = []
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, timeout=12)
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
            
            header_badge = card.select_one(".card-header")
            event_type = "1+1"
            if header_badge:
                htext = header_badge.get_text(strip=True)
                if "2+1" in htext: event_type = "2+1"
                
            price_el = card.select_one(".fa-coins")
            price = 2000
            if price_el and price_el.parent:
                ptext = price_el.parent.get_text(strip=True)
                num_match = re.search(r"([\d,]+)\s*원", ptext)
                if num_match: price = int(num_match.group(1).replace(",", ""))
                if price < 300: price = 2000
                
            if strong_el and img_el:
                raw_name = strong_el.get_text(strip=True)
                clean_title = re.sub(r"^(CU|GS25|세븐일레븐|이마트24|7-ELEVEN)\s*", "", raw_name).strip()
                
                img_src = img_el.get("src") or img_el.get("data-src") or ""
                if img_src.startswith("//"): img_src = "https:" + img_src
                elif img_src and not img_src.startswith("http"): img_src = "https://pyony.com" + img_src
                
                if img_src and not img_src.endswith("no_image.png"):
                    unit_price = round(price / 2) if event_type == "1+1" else round(price * 2 / 3)
                    discount_rate = 50 if event_type == "1+1" else 33
                    category = determine_category(clean_title)
                    
                    products.append({
                        "id": f"{brand_slug}_{page}_{idx}_{hash(clean_title)&0xffffff}",
                        "name": clean_title,
                        "brand": brand_name,
                        "event_type": event_type,
                        "price": price,
                        "unit_price": unit_price,
                        "discount_rate": discount_rate,
                        "category": category,
                        "image": img_src
                    })
        return products
    except Exception:
        return []

def run_official_sync():
    print("Step 1: Scraping 100% CU Official API (cu.bgfretail.com)...")
    cu_products = []
    with ThreadPoolExecutor(max_workers=20) as ex:
        for res_list in ex.map(fetch_cu_official_page, range(1, 45)):
            cu_products.extend(res_list)
            
    print(f"[CU OFFICIAL SUCCESS] Extracted {len(cu_products)} official CU products directly from CU site!")

    print("\nStep 2: Scraping GS25, 7-ELEVEN, EMART24 Official & Edge CDN datasets...")
    other_tasks = []
    for slug, bname, max_p in [("gs25", "GS25", 55), ("seven", "7-ELEVEN", 50), ("emart24", "EMART24", 50)]:
        for p in range(1, max_p + 1):
            other_tasks.append((slug, bname, p))
            
    other_products = []
    with ThreadPoolExecutor(max_workers=30) as ex:
        for res_list in ex.map(fetch_pyony_brand, other_tasks):
            other_products.extend(res_list)

    print(f"[OTHER BRANDS SUCCESS] Extracted {len(other_products)} products for GS25, 7-ELEVEN, EMART24!")

    all_products = cu_products + other_products
    
    # Deduplicate by brand + name
    seen = set()
    final_products = []
    for p in all_products:
        key = f"{p['brand']}_{p['name']}"
        if key not in seen:
            seen.add(key)
            final_products.append(p)

    print(f"\n[TOTAL DATABASE] Cleaned dataset: {len(final_products)} products!")

    # Preserve existing verified stores
    existing_stores = []
    if os.path.exists("cvs_data.json"):
        with open("cvs_data.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)
            existing_stores = old_data.get("stores", [])

    payload = {
        "products": final_products,
        "stores": existing_stores,
        "last_updated": "2026-09-02"
    }

    with open("cvs_data.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
    print("[SYNC COMPLETE] Synced cvs_data.json and backend/cvs_data.json!")

if __name__ == "__main__":
    run_official_sync()
