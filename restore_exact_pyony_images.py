import json
import urllib.request
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

BRANDS = [
    ("cu", "CU", 50),
    ("gs25", "GS25", 40),
    ("seven", "7-ELEVEN", 35),
    ("emart24", "EMART24", 35)
]

def crawl_exact_page(args):
    brand_slug, brand_name, page = args
    url = f"https://pyony.com/brands/{brand_slug}/?page={page}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".col-md-6") or soup.select(".card")
        results = {}
        
        for card in cards:
            strong_el = card.select_one(".card-body strong") or card.select_one("strong")
            img_el = card.select_one("img.prod_img") or card.select_one("img")
            
            if strong_el and img_el:
                raw_name = strong_el.get_text(strip=True)
                clean_key = re.sub(r"[^a-zA-Z0-9가-힣]", "", raw_name)
                
                img_url = img_el.get("src") or img_el.get("data-src") or ""
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                elif img_url and not img_url.startswith("http"):
                    img_url = "https://pyony.com" + img_url
                    
                if img_url:
                    results[clean_key] = img_url
        return results
    except Exception as e:
        return {}

def restore_exact():
    print("Scraping 100% official product packaging images with fuzzy key normalization...")
    tasks = []
    for slug, bname, max_p in BRANDS:
        for p in range(1, max_p + 1):
            tasks.append((slug, bname, p))
            
    official_map = {}
    with ThreadPoolExecutor(max_workers=30) as executor:
        for res in executor.map(crawl_exact_page, tasks):
            official_map.update(res)
            
    print(f"\n[FETCHED] Obtained {len(official_map)} official product packaging CDN images!")

    with open("cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    restored_count = 0

    for p in products:
        pname = p.get("name", "")
        clean_pname = re.sub(r"[^a-zA-Z0-9가-힣]", "", pname)
        
        # Match normalized key
        matched_url = None
        if clean_pname in official_map:
            matched_url = official_map[clean_pname]
        else:
            for k, v in official_map.items():
                if len(k) > 4 and (k in clean_pname or clean_pname in k):
                    matched_url = v
                    break
                    
        if matched_url:
            p["image"] = matched_url
            restored_count += 1

    print(f"[EXACT RESTORED] Updated {restored_count} product images with official product packaging CDN URLs!")

    for target in ["cvs_data.json", "backend/cvs_data.json"]:
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    restore_exact()
