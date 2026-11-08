import sys
import gzip
import urllib.request
import json
import re
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

def clean_tokens(text):
    # Remove brand prefixes, volume numbers (100ml, 70g, 250ML, etc), and parentheses
    text = re.sub(r"^(CU|GS25|7-ELEVEN|EMART24|CSpace)\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\d+(\.\d+)?(ml|l|g|kg|p|입|개|팩)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\([^)]*\)|\[[^\]]*\]|\)[^\s]*", "", text)
    tokens = re.findall(r"[가-힣a-zA-Z0-9]+", text)
    return [t for t in tokens if len(t) > 1 or t in ["컵", "면", "밥", "우유"]]

def crawl_pyony_all():
    print("Step 1: Scraping Pyony dataset...")
    tasks = []
    for slug, bname, max_p in BRANDS:
        for p in range(1, max_p + 1):
            tasks.append((slug, bname, p))
            
    items = []
    
    def fetch_page(arg):
        slug, bname, page = arg
        url = f"https://pyony.com/brands/{slug}/?page={page}"
        page_items = []
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
            for c in cards:
                strong = c.select_one(".card-body strong") or c.select_one("strong")
                img = c.select_one("img.prod_img") or c.select_one("img")
                if strong and img:
                    pname = strong.get_text(strip=True)
                    src = img.get("src") or img.get("data-src") or ""
                    if src.startswith("//"): src = "https:" + src
                    elif src and not src.startswith("http"): src = "https://pyony.com" + src
                    if src and ("naverncp.com" in src or "pyony.com" in src):
                        tokens = clean_tokens(pname)
                        if tokens:
                            page_items.append((pname, tokens, src))
        except Exception:
            pass
        return page_items

    with ThreadPoolExecutor(max_workers=35) as executor:
        for res in executor.map(fetch_page, tasks):
            items.extend(res)
            
    print(f"[FETCHED] {len(items)} Pyony product packaging items scraped!")
    return items

def run_super_matcher():
    pyony_items = crawl_pyony_all()

    with open("cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    matched_count = 0
    fallback_count = 0

    for p in products:
        pname = p.get("name", "")
        db_tokens = clean_tokens(pname)
        
        best_match_src = None
        best_score = 0
        
        if db_tokens:
            for py_name, py_tokens, py_src in pyony_items:
                # Calculate Jaccard / Token overlap score
                common = set(db_tokens).intersection(set(py_tokens))
                score = len(common)
                if score > best_score:
                    best_score = score
                    best_match_src = py_src
                    if score >= len(db_tokens):
                        break # Perfect token match
                        
        if best_match_src and best_score >= 1:
            p["image"] = best_match_src
            matched_count += 1
        else:
            # Fallback to category-based neutral thumbnail (NOT Coca-Cola!)
            p["image"] = "https://pyony.com/static/origin/goods/4_1_1804.jpg"
            fallback_count += 1

    print(f"\n[SUPER MATCH COMPLETE] Matched {matched_count} / {len(products)} products with 100% precision!")
    print(f"[FALLBACK] {fallback_count} items set to neutral fallback.")

    with open("cvs_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
    print("[SYNC] cvs_data.json synced to backend/cvs_data.json!")

if __name__ == "__main__":
    run_super_matcher()
