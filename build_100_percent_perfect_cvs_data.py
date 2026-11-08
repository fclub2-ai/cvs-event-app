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

def crawl_pyony_page(args):
    brand_slug, brand_name, page = args
    url = f"https://pyony.com/brands/{brand_slug}/?page={page}"
    results = {}
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, timeout=12)
        raw_data = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            html = gzip.decompress(raw_data).decode('utf-8', errors='ignore')
        else:
            html = raw_data.decode('utf-8', errors='ignore')
            
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".col-md-6") or soup.select(".card")
        
        for card in cards:
            strong_el = card.select_one(".card-body strong") or card.select_one("strong")
            img_el = card.select_one("img.prod_img") or card.select_one("img")
            
            if strong_el and img_el:
                pname = strong_el.get_text(strip=True)
                img_src = img_el.get("src") or img_el.get("data-src") or ""
                if img_src.startswith("//"):
                    img_src = "https:" + img_src
                elif img_src and not img_src.startswith("http"):
                    img_src = "https://pyony.com" + img_src
                    
                if img_src and ("naverncp.com" in img_src or "pyony.com" in img_src):
                    # Clean normalized key for fuzzy matching
                    full_pname = f"{brand_name} {pname}"
                    clean_full = re.sub(r"[^a-zA-Z0-9가-힣]", "", full_pname)
                    clean_name_only = re.sub(r"[^a-zA-Z0-9가-힣]", "", pname)
                    
                    results[clean_full] = img_src
                    results[clean_name_only] = img_src
        return results
    except Exception as e:
        return {}

def run_master_build():
    print("Step 1: Crawling 100% Pyony product packaging images with UTF-8 gzip...")
    tasks = []
    for slug, bname, max_p in BRANDS:
        for p in range(1, max_p + 1):
            tasks.append((slug, bname, p))
            
    pyony_map = {}
    with ThreadPoolExecutor(max_workers=35) as executor:
        for res in executor.map(crawl_pyony_page, tasks):
            pyony_map.update(res)
            
    print(f"\n[SUCCESS] Extracted {len(pyony_map)} clean product packaging CDN URLs from Pyony!")

    # Step 2: Load cvs_data.json
    with open("cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    matched_count = 0
    fallback_count = 0

    # Brand color badge clean placeholders for unmatched items (NO Coca-Cola!)
    BRAND_PLACEHOLDERS = {
        "GS25": "https://pyony.com/static/origin/goods/4_1_1804.jpg",
        "CU": "https://pyony.com/static/origin/goods/4_1_1805.jpg",
        "7-ELEVEN": "https://pyony.com/static/origin/goods/4_1_1806.jpg",
        "EMART24": "https://pyony.com/static/origin/goods/4_1_1807.jpg"
    }

    for p in products:
        pname = p.get("name", "")
        brand = p.get("brand", "GS25")
        
        clean_target = re.sub(r"[^a-zA-Z0-9가-힣]", "", pname)
        
        # 1. Direct exact key match
        matched_url = pyony_map.get(clean_target)
        
        # 2. Substring fuzzy match
        if not matched_url:
            for k, v in pyony_map.items():
                if len(k) >= 4 and (k in clean_target or clean_target in k):
                    matched_url = v
                    break
                    
        if matched_url:
            p["image"] = matched_url
            matched_count += 1
        else:
            # Fallback to category/brand placeholder, NEVER Coca-Cola!
            p["image"] = BRAND_PLACEHOLDERS.get(brand, BRAND_PLACEHOLDERS["GS25"])
            fallback_count += 1

    print(f"[MATCH COMPLETE] Matched {matched_count} / {len(products)} products to real packaging photos!")
    print(f"[FALLBACK COMPLETE] Set clean brand fallback for {fallback_count} remaining items.")

    # Save to both locations
    with open("cvs_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
    print("[SYNC COMPLETE] Synced cvs_data.json to backend/cvs_data.json!")

if __name__ == "__main__":
    run_master_build()
