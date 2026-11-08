import urllib.request
import urllib.parse
import json
import re
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded"
}

def crawl_cu_page(args):
    event_code, event_type, page = args
    url = "https://cu.bgfretail.com/event/plusAjax.do"
    data = urllib.parse.urlencode({
        "pageIndex": page,
        "listType": 1,
        "searchCondition": "",
        "user_id": "",
        "eventCd": event_code
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=data, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=6).read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("li")
        results = []
        for item in items:
            name_el = item.select_one(".name")
            price_el = item.select_one(".price")
            img_el = item.select_one("img")
            if name_el and price_el:
                name = name_el.get_text(strip=True)
                price_text = re.sub(r"[^\d]", "", price_el.get_text(strip=True))
                price = int(price_text) if price_text else 2000
                img = img_el.get("src") if img_el else ""
                if img and not img.startswith("http"):
                    img = "https:" + img if img.startswith("//") else "https://cu.bgfretail.com" + img
                
                results.append({
                    "name": f"CU {name}",
                    "brand": "CU",
                    "price": price,
                    "unit_price": round(price / 2 if event_type == "1+1" else price * 2 / 3),
                    "discount_rate": 50 if event_type == "1+1" else 33,
                    "event_type": event_type,
                    "category": "음료/스낵",
                    "image": img
                })
        return results
    except Exception:
        return []

def crawl_7eleven_page(args):
    p_tab, event_type, page = args
    url = "https://www.7-eleven.co.kr/product/presentList.asp"
    data = urllib.parse.urlencode({
        "pTab": p_tab,
        "intPageSize": 40,
        "intPageNo": page
    }).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=6).read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".pic_product")
        results = []
        for item in items:
            name_el = item.select_one(".name")
            price_el = item.select_one(".price")
            img_el = item.select_one("img")
            if name_el and price_el:
                name = name_el.get_text(strip=True)
                price_text = re.sub(r"[^\d]", "", price_el.get_text(strip=True))
                price = int(price_text) if price_text else 1800
                img = img_el.get("src") if img_el else ""
                if img and not img.startswith("http"):
                    img = "https://www.7-eleven.co.kr" + img
                
                results.append({
                    "name": f"세븐일레븐 {name}",
                    "brand": "7-ELEVEN",
                    "price": price,
                    "unit_price": round(price / 2 if event_type == "1+1" else price * 2 / 3),
                    "discount_rate": 50 if event_type == "1+1" else 33,
                    "event_type": event_type,
                    "category": "스낵/과자",
                    "image": img
                })
        return results
    except Exception:
        return []

def main():
    print("Starting ultra-fast parallel multi-page crawl...")
    tasks_cu = []
    for code, etype in [("1", "1+1"), ("2", "2+1")]:
        for p in range(1, 26):
            tasks_cu.append((code, etype, p))

    tasks_7eleven = []
    for tab, etype in [("1", "1+1"), ("2", "2+1")]:
        for p in range(1, 26):
            tasks_7eleven.append((tab, etype, p))

    all_products = []
    with ThreadPoolExecutor(max_workers=25) as executor:
        res_cu = executor.map(crawl_cu_page, tasks_cu)
        for rList in res_cu:
            all_products.extend(rList)

        res_7 = executor.map(crawl_7eleven_page, tasks_7eleven)
        for rList in res_7:
            all_products.extend(rList)

    # Deduplicate products by name
    seen = set()
    unique_products = []
    for p in all_products:
        if p["name"] not in seen:
            seen.add(p["name"])
            unique_products.append(p)

    print(f"Scraped {len(unique_products)} unique live products!")

    # Merge with existing cvs_data.json
    with open("cvs_data.json", "r", encoding="utf-8") as f:
        existing_data = json.load(f)

    existing_items = existing_data.get("products", existing_data) if isinstance(existing_data, dict) else existing_data
    existing_names = set(p["name"] for p in existing_items)

    added_count = 0
    for p in unique_products:
        if p["name"] not in existing_names:
            existing_items.append(p)
            existing_names.add(p["name"])
            added_count += 1

    print(f"Added {added_count} new items! Total catalog dataset size: {len(existing_items)} items!")

    if isinstance(existing_data, dict):
        existing_data["products"] = existing_items
    else:
        existing_data = existing_items

    for target in ["cvs_data.json", "backend/cvs_data.json"]:
        with open(target, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

    import subprocess
    subprocess.run(["python", "build_full_bundle.py"])
    subprocess.run(["python", "create_zip_package.py"])
    print("[SUCCESS] Rebuilt dataset, index.html bundle, and ZIP package!")

if __name__ == "__main__":
    main()
