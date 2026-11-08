"""
Step 2: 312개 상품에서 고유 상품 base name 추출 (브랜드 접두사 제거)
"""
import json
import re

DATA_FILE = r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", [])

# Extract unique base product names (remove brand prefix like "GS25) ", "CU) " etc)
unique_bases = {}
for p in products:
    name = p["name"]
    # Remove brand prefix
    base = re.sub(r'^(GS25|CU|7-ELEVEN|EMART24)\)\s*', '', name)
    if base not in unique_bases:
        unique_bases[base] = {
            "category": p["category"],
            "current_image": p["image"],
            "has_imgbb": "ibb.co" in p.get("image", ""),
            "ids": []
        }
    unique_bases[base]["ids"].append(p["id"])

print(f"Total products: {len(products)}")
print(f"Unique base products: {len(unique_bases)}")
print(f"Already on ImgBB: {sum(1 for v in unique_bases.values() if v['has_imgbb'])}")
print(f"Need ImgBB upload: {sum(1 for v in unique_bases.values() if not v['has_imgbb'])}")
print()

# List all unique products that need images
for i, (base, info) in enumerate(unique_bases.items()):
    status = "IMGBB" if info["has_imgbb"] else "NEED"
    print(f"  [{status}] {base} ({info['category']}) - {len(info['ids'])} variants")
