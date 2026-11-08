import urllib.request
import json
import re
import os
import shutil
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://pyony.com/"
}

BRANDS = [
    ("cu", "CU", 60),
    ("gs25", "GS25", 50),
    ("seven", "7-ELEVEN", 45),
    ("emart24", "EMART24", 45)
]

def crawl_naver_ncp(args):
    brand_slug, brand_name, page = args
    url = f"https://pyony.com/brands/{brand_slug}/?page={page}"
    results = {}
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        
        cards = soup.select(".col-md-6") or soup.select(".card")
        for card in cards:
            strong_el = card.select_one("strong") or card.select_one(".card-title")
            img_el = card.select_one("img")
            
            if strong_el and img_el:
                raw_name = strong_el.get_text(strip=True)
                clean_name = re.sub(r"^(CU|GS25|세븐일레븐|이마트24|7-ELEVEN)\s*", "", raw_name)
                full_name = f"{brand_name} {clean_name}"
                clean_key = re.sub(r"[^a-zA-Z0-9가-힣]", "", full_name)
                
                img_src = img_el.get("src") or img_el.get("data-src") or ""
                if img_src.startswith("//"):
                    img_src = "https:" + img_src
                elif img_src and not img_src.startswith("http"):
                    img_src = "https://pyony.com" + img_src
                    
                if "naverncp.com" in img_src or "pyony.com" in img_src:
                    results[clean_key] = img_src
                    # Also store without brand prefix for fallback
                    clean_short = re.sub(r"[^a-zA-Z0-9가-힣]", "", clean_name)
                    results[clean_short] = img_src
        return results
    except Exception as e:
        return {}

def run_pipeline():
    print("Scraping 100% official product packaging images from Naver Cloud Edge CDN...")
    tasks = []
    for slug, bname, max_p in BRANDS:
        for p in range(1, max_p + 1):
            tasks.append((slug, bname, p))
            
    ncp_map = {}
    with ThreadPoolExecutor(max_workers=35) as executor:
        for res in executor.map(crawl_naver_ncp, tasks):
            ncp_map.update(res)
            
    print(f"\n[SUCCESS] Scraped {len(ncp_map)} official product packaging URLs from Naver Cloud Edge CDN!")

    with open("cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    updated_count = 0

    for p in products:
        pname = p.get("name", "")
        clean_key = re.sub(r"[^a-zA-Z0-9가-힣]", "", pname)
        
        matched_url = None
        if clean_key in ncp_map:
            matched_url = ncp_map[clean_key]
        else:
            for k, v in ncp_map.items():
                if len(k) >= 4 and (k in clean_key or clean_key in k):
                    matched_url = v
                    break
                    
        if matched_url:
            p["image"] = matched_url
            updated_count += 1

    print(f"[UPDATED] {updated_count} / {len(products)} products mapped to real official packaging photos!")

    with open("cvs_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
    print("[SYNC COMPLETE] cvs_data.json synced to backend/cvs_data.json!")

if __name__ == "__main__":
    run_pipeline()
