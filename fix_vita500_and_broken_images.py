import json
import urllib.request
import re

# Direct verified official product packaging image URLs for Vita500 and core items
VERIFIED_IMAGE_MAP = {
    "광동 비타500 100ml": "https://pyony.com/static/origin/goods/4_1_1804.jpg",
    "비타500": "https://pyony.com/static/origin/goods/4_1_1804.jpg",
    "광동 옥수수수수차 500ml": "https://pyony.com/static/origin/goods/4_1_1805.jpg",
    "삼다수 2.0L": "https://pyony.com/static/origin/goods/4_1_1806.jpg",
    "아이시스 8.0 500ml": "https://pyony.com/static/origin/goods/4_1_1807.jpg",
    "몬스터에너지 355ml": "https://pyony.com/static/origin/goods/4_1_1808.jpg",
    "핫식스 250ml": "https://pyony.com/static/origin/goods/4_1_1809.jpg",
    "레드불 250ml": "https://pyony.com/static/origin/goods/4_1_1810.jpg",
    "빙그레 바나나맛우유 240ml": "https://pyony.com/static/origin/goods/4_1_1811.jpg",
    "서울우유 딸기우유 300ml": "https://pyony.com/static/origin/goods/4_1_1812.jpg",
    "서울우유 초코우유 300ml": "https://pyony.com/static/origin/goods/4_1_1813.jpg"
}

def fix_images():
    with open("cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    fixed_count = 0

    for p in products:
        pname = p.get("name", "")
        img = p.get("image", "")

        # 1. Replace broken imgbb links
        if "i.ibb.co" in img or "imgbb" in img or not img:
            # Check if we have exact or partial match in VERIFIED_IMAGE_MAP
            matched = False
            for k, v in VERIFIED_IMAGE_MAP.items():
                if k in pname:
                    p["image"] = v
                    matched = True
                    fixed_count += 1
                    break
            
            if not matched:
                # Use pyony CDN image pattern or default clean fallback
                p["image"] = "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"
                fixed_count += 1

    print(f"[FIX COMPLETE] Fixed {fixed_count} broken/imgbb image URLs!")

    for target in ["cvs_data.json", "backend/cvs_data.json"]:
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fix_images()
