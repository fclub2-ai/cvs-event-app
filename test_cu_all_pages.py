import urllib.request
import urllib.parse
import json
import re
import subprocess
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Content-Type": "application/x-www-form-urlencoded"
}

def fetch_all_cu_events():
    cu_products = []
    url = "https://cu.bgfretail.com/event/plusAjax.do"
    
    for event_code, event_type in [("1", "1+1"), ("2", "2+1")]:
        print(f"[CU] Fetching all pages for {event_type}...")
        page = 1
        while page <= 30: # Up to 30 pages per category
            cmd = [
                "curl.exe", "-s", "-L",
                "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "-H", "Content-Type: application/x-www-form-urlencoded",
                "-d", f"pageIndex={page}&listType=1&searchCondition=&user_id=&eventCd={event_code}",
                url
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
            html = res.stdout
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select("li")
            if not items:
                print(f"  -> No more items at page {page}")
                break
                
            count = 0
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
                    
                    cu_products.append({
                        "name": f"CU {name}",
                        "brand": "CU",
                        "price": price,
                        "unit_price": round(price / 2 if event_type == "1+1" else price * 2 / 3),
                        "discount_rate": 50 if event_type == "1+1" else 33,
                        "event_type": event_type,
                        "category": "음료/간식",
                        "image": img
                    })
                    count += 1
            print(f"  Page {page}: fetched {count} items")
            page += 1
    return cu_products

if __name__ == "__main__":
    products = fetch_all_cu_events()
    print(f"\n[CU TOTAL] Fetched {len(products)} live event items!")
