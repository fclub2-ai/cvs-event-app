import json
import urllib.request
import urllib.parse
import base64
import sys

DATA_FILE = r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json"
ROOT_DATA_FILE = r"C:\Users\fclub\cvs-event-app\cvs_data.json"

IMGBB_API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", [])

import re
unique_bases = {}
for p in products:
    base = re.sub(r'^(GS25|CU|7-ELEVEN|EMART24)\)\s*', '', p["name"])
    if base not in unique_bases:
        unique_bases[base] = p["image"]

print(f"Total unique products: {len(unique_bases)}", flush=True)

# High-reliability Unsplash direct image sources for fallback re-uploads
REPLACE_SOURCES = {
    "비타500": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=500",
    "맥스웰": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500",
    "초코송이": "https://images.unsplash.com/photo-1582176604856-e822b3749c6c?w=500",
    "신라면": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500",
    "진라면": "https://images.unsplash.com/photo-1612927601601-6638404737ce?w=500",
    "불닭": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=500",
    "짜파게티": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500",
    "육개장": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500",
    "참깨라면": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500",
    "햇반": "https://images.unsplash.com/photo-1516714435131-44d6b64dc6a2?w=500",
    "오뚜기밥": "https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=500",
    "도시락": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500",
    "떡볶이": "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?w=500",
    "만두": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=500",
    "크래미": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=500",
    "스팸": "https://images.unsplash.com/photo-1544025162-d76694265947?w=500",
    "참치": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=500",
    "피자": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500",
    "바나나": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=500",
    "딸기": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=500",
    "초코": "https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=500",
    "커피": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500",
    "액티비아": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500",
    "요거톡": "https://images.unsplash.com/photo-1571212515416-fef01fc43637?w=500",
    "포카칩": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=500",
    "꼬북칩": "https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=500",
    "허니버터칩": "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?w=500",
    "새우깡": "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?w=500",
    "빼빼로": "https://images.unsplash.com/photo-1541781774459-bb29b565090c?w=500",
    "가나": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=500",
    "페레로로쉐": "https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=500",
    "하리보": "https://images.unsplash.com/photo-1582058091505-f87a2e55a40f?w=500",
    "초코파이": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500",
    "칙촉": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=500",
    "치약": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=500",
    "칫솔": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=500",
    "샴푸": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=500",
    "세제": "https://images.unsplash.com/photo-1584813470613-5a1c1cad3d69?w=500",
    "생리대": "https://images.unsplash.com/photo-1584556812952-905ffd0c611a?w=500",
    "구강": "https://images.unsplash.com/photo-1559598467-f8b76c8155d0?w=500",
    "페브리즈": "https://images.unsplash.com/photo-1616401784845-180882ba9ba8?w=500",
    "다우니": "https://images.unsplash.com/photo-1584813470613-5a1c1cad3d69?w=500",
    "컨디션": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500",
    "여명": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500",
    "콜라": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    "사이다": "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=500",
    "삼다수": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=500",
}

DEFAULT_SRC = "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500"

def upload_imgbb(b64_data, name="product"):
    try:
        payload = urllib.parse.urlencode({
            "key": IMGBB_API_KEY,
            "image": b64_data,
            "name": name,
        }).encode("utf-8")
        req = urllib.request.Request("https://api.imgbb.com/1/upload", data=payload, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if res.get("success"):
                return res["data"]["url"]
    except Exception as e:
        print(f"    Upload Error: {e}", flush=True)
    return None

fixed_map = {}

for name, url in unique_bases.items():
    is_ok = False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                is_ok = True
    except:
        is_ok = False

    if is_ok:
        print(f"[OK] {name}", flush=True)
    else:
        print(f"[FIXING 404] {name}...", flush=True)
        src = DEFAULT_SRC
        for kw, r_src in REPLACE_SOURCES.items():
            if kw in name:
                src = r_src
                break
        try:
            req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                b64_str = base64.b64encode(resp.read()).decode("utf-8")
                new_url = upload_imgbb(b64_str, name[:15])
                if new_url:
                    fixed_map[name] = new_url
                    print(f"   -> NEW IMGBB URL: {new_url}", flush=True)
        except Exception as e:
            print(f"   -> FAILED: {e}", flush=True)

# Apply fixes
for p in products:
    base = re.sub(r'^(GS25|CU|7-ELEVEN|EMART24)\)\s*', '', p["name"])
    if base in fixed_map:
        p["image"] = fixed_map[base]

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open(ROOT_DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n[DONE] Fixed {len(fixed_map)} broken 404 URLs!", flush=True)
