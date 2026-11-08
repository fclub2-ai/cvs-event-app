import json

with open("cvs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", data) if isinstance(data, dict) else data

unique_items = []
seen = set()

for p in products:
    name = p["name"]
    base_name = name.split(") ")[-1] if ") " in name else name
    if base_name not in seen:
        seen.add(base_name)
        unique_items.append({
            "base_name": base_name,
            "category": p.get("category", ""),
            "sample_full_name": name,
            "current_image": p.get("image", "")
        })

with open("unique_78.json", "w", encoding="utf-8") as f:
    json.dump(unique_items, f, ensure_ascii=False, indent=2)

print(f"Dumped {len(unique_items)} unique base products to unique_78.json")
