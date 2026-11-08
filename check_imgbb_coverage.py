import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", [])

import re
unique_bases = {}
for p in products:
    base = re.sub(r'^(GS25|CU|7-ELEVEN|EMART24)\)\s*', '', p["name"])
    if base not in unique_bases:
        unique_bases[base] = p["image"]

print(f"Total products: {len(products)}")
print(f"Total unique product names: {len(unique_bases)}")

imgbb_items = []
non_imgbb_items = []

for base, img in unique_bases.items():
    if "ibb.co" in img:
        imgbb_items.append((base, img))
    else:
        non_imgbb_items.append((base, img))

print(f"ImgBB items: {len(imgbb_items)}")
print(f"Non-ImgBB items: {len(non_imgbb_items)}")
print("\n--- Non-ImgBB Items List ---")
for name, img in non_imgbb_items:
    print(f"Name: {name} | Image: {img}")
