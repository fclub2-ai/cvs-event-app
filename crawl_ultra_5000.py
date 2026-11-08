import urllib.request
import urllib.parse
import json
import re
import os
import subprocess
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

BRANDS = [
    ("cu", "CU", 70),
    ("gs25", "GS25", 60),
    ("seven", "7-ELEVEN", 50),
    ("emart24", "EMART24", 50),
    ("cspace", "CSpace", 20)
]

def crawl_ultra_page(args):
    brand_slug, brand_name, page = args
    url = f"https://pyony.com/brands/{brand_slug}/?page={page}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".col-md-6") or soup.select(".card")
        results = []
        
        for card in cards:
            strong_el = card.select_one(".card-body strong") or card.select_one("strong")
            img_el = card.select_one("img.prod_img") or card.select_one("img")
            cat_el = card.select_one(".card-header small.font-weight-bold")
            badge_el = card.select_one(".badge")
            
            if strong_el and img_el:
                raw_name = strong_el.get_text(strip=True)
                clean_name = re.sub(r"^(CU|GS25|세븐일레븐|이마트24|7-ELEVEN|씨스페이스|CSpace)\s*", "", raw_name)
                full_name = f"{brand_name} {clean_name}"
                
                category = cat_el.get_text(strip=True) if cat_el else "식품/간편식"
                
                event_type = "1+1"
                if badge_el:
                    btext = badge_el.get_text(strip=True)
                    if "2+1" in btext:
                        event_type = "2+1"
                    elif "3+1" in btext:
                        event_type = "3+1"
                    elif "할인" in btext:
                        event_type = "할인"
                        
                card_text = card.get_text()
                price_match = re.search(r"([\d,]+)\s*원", card_text)
                price = 2000
                if price_match:
                    p_str = price_match.group(1).replace(",", "")
                    if p_str.isdigit() and int(p_str) > 100:
                        price = int(p_str)
                        
                img_url = img_el.get("src") or img_el.get("data-src") or ""
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                elif img_url and not img_url.startswith("http"):
                    img_url = "https://pyony.com" + img_url
                    
                if event_type == "1+1":
                    unit_price = round(price / 2)
                    discount_rate = 50
                elif event_type == "2+1":
                    unit_price = round(price * 2 / 3)
                    discount_rate = 33
                else:
                    unit_price = round(price * 3 / 4)
                    discount_rate = 25
                    
                results.append({
                    "name": full_name,
                    "brand": brand_name,
                    "price": price,
                    "unit_price": unit_price,
                    "discount_rate": discount_rate,
                    "event_type": event_type,
                    "category": category,
                    "image": img_url
                })
        return results
    except Exception as e:
        return []

def main():
    print("Executing ULTRA MAXIMUM CRAWL across all 5 brands up to page 70...")
    tasks = []
    for slug, bname, max_p in BRANDS:
        for p in range(1, max_p + 1):
            tasks.append((slug, bname, p))
            
    scraped_items = []
    with ThreadPoolExecutor(max_workers=35) as executor:
        for result in executor.map(crawl_ultra_page, tasks):
            scraped_items.extend(result)
            
    seen = set()
    unique_items = []
    for item in scraped_items:
        if item["name"] not in seen:
            seen.add(item["name"])
            unique_items.append(item)
            
    print(f"\n[ULTRA CRAWL SUCCESS] Scraped {len(unique_items)} total live deal items!")
    
    # Read existing
    with open("cvs_data.json", "r", encoding="utf-8") as f:
        existing_data = json.load(f)

    existing_items = existing_data.get("products", []) if isinstance(existing_data, dict) else existing_data
    existing_stores = existing_data.get("stores", []) if isinstance(existing_data, dict) else []
    existing_names = set(p["name"] for p in existing_items)

    added_count = 0
    for p in unique_items:
        if p["name"] not in existing_names:
            existing_items.append(p)
            existing_names.add(p["name"])
            added_count += 1

    print(f"Added {added_count} new items! Total catalog dataset size: {len(existing_items)} items!")

    final_data = {
        "products": existing_items,
        "stores": existing_stores
    }

    for target in ["cvs_data.json", "backend/cvs_data.json"]:
        with open(target, "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)

    subprocess.run(["python", "build_full_bundle.py"])
    subprocess.run(["python", "create_zip_package.py"])
    print(f"\n[ULTRA COMPLETE] Catalog expanded to {len(existing_items)} items! Bundled ZIP generated!")

if __name__ == "__main__":
    main()
