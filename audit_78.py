import json
from collections import defaultdict

with open("cvs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", data) if isinstance(data, dict) else data

base_to_img = {}
img_to_bases = defaultdict(list)

for p in products:
    name = p["name"]
    base_name = name.split(") ")[-1] if ") " in name else name
    img = p.get("image", "")
    base_to_img[base_name] = img
    if base_name not in img_to_bases[img]:
        img_to_bases[img].append(base_name)

print(f"Total unique products: {len(base_to_img)}")
print(f"Total unique image URLs: {len(img_to_bases)}")

print("\n--- Shared Image URLs (Duplicates) ---")
for img, bases in img_to_bases.items():
    if len(bases) > 1:
        print(f"\nImage URL: {img} (Used by {len(bases)} products):")
        for b in bases:
            print("  -", b)

print("\n--- Single-use (Unique) Image URLs ---")
unique_ok = 0
for img, bases in img_to_bases.items():
    if len(bases) == 1:
        unique_ok += 1
        print(f"  [OK] {bases[0]} -> {img}")

print(f"\nSummary: {unique_ok} products have unique image URLs, {78 - unique_ok} products share duplicate fallback images.")
