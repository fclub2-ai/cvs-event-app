import urllib.request
import urllib.parse
import json
import re
import subprocess
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

def fetch_all_cu():
    cu_products = []
    url = "https://cu.bgfretail.com/event/plusAjax.do"
    for event_code, event_type in [("1", "1+1"), ("2", "2+1")]:
        page = 1
        while page <= 15: # 15 pages * 40 items = 600 per category
            cmd = [
                "curl.exe", "-s", "-L",
                "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "-H", "Content-Type: application/x-www-form-urlencoded",
                "-d", f"pageIndex={page}&listType=1&searchCondition=&user_id=&eventCd={event_code}",
                url
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(res.stdout, "html.parser")
            items = soup.select("li")
            if not items:
                break
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
                        "category": "음료/스낵",
                        "image": img
                    })
            page += 1
    return cu_products

def fetch_all_7eleven():
    seven_products = []
    url = "https://www.7-eleven.co.kr/product/presentList.asp"
    for p_tab, event_type in [("1", "1+1"), ("2", "2+1")]:
        page = 1
        while page <= 15:
            cmd = [
                "curl.exe", "-s", "-L",
                "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "-H", "Content-Type: application/x-www-form-urlencoded",
                "-d", f"pTab={p_tab}&intPageSize=40&intPageNo={page}",
                url
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(res.stdout, "html.parser")
            items = soup.select(".pic_product")
            if not items:
                break
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
                    
                    seven_products.append({
                        "name": f"세븐일레븐 {name}",
                        "brand": "7-ELEVEN",
                        "price": price,
                        "unit_price": round(price / 2 if event_type == "1+1" else price * 2 / 3),
                        "discount_rate": 50 if event_type == "1+1" else 33,
                        "event_type": event_type,
                        "category": "스낵/과자",
                        "image": img
                    })
            page += 1
    return seven_products

if __name__ == "__main__":
    cu = fetch_all_cu()
    seven = fetch_all_7eleven()
    print(f"CU: {len(cu)} items")
    print(f"7-ELEVEN: {len(seven)} items")
    print(f"Total live scraped: {len(cu) + len(seven)} items!")
