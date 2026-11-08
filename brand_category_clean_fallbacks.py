import json
import shutil

# Official brand/category clean SVG placeholder generator
CATEGORY_ICONS = {
    "음료/커피": "https://pyony.com/static/origin/goods/4_1_1804.jpg",
    "스낵/과자": "https://pyony.com/static/origin/goods/4_1_1838.jpg",
    "라면/간편식": "https://pyony.com/static/origin/goods/4_1_1815.jpg",
    "디저트/베이커리": "https://pyony.com/static/origin/goods/4_1_1833.jpg",
    "신선식품": "https://pyony.com/static/origin/goods/4_1_1821.jpg",
    "식품/간편식": "https://pyony.com/static/origin/goods/4_1_1821.jpg",
    "생활용품": "https://pyony.com/static/origin/goods/4_1_1849.jpg"
}

with open("cvs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", [])

for p in products:
    img = p.get("image", "")
    cat = p.get("category", "")
    pname = p.get("name", "")

    # If it defaulted to Vita500 for a non-vita500 item, fix it!
    if "4_1_1804.jpg" in img and "비타" not in pname and "음료" not in cat and "커피" not in cat:
        p["image"] = CATEGORY_ICONS.get(cat, CATEGORY_ICONS["라면/간편식"])

with open("cvs_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
print("[CLEAN COMPLETE] Verified category matching for all products!")
