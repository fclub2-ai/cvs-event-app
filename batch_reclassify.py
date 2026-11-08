import json
import os
from sync_official_cvs_data import determine_category

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILES = [
    os.path.join(BASE_DIR, "cvs_data.json"),
    os.path.join(BASE_DIR, "backend", "cvs_data.json")
]

for file_path in DATA_FILES:
    if not os.path.exists(file_path):
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    count_changed = 0
    for p in data.get("products", []):
        old_cat = p.get("category", "")
        new_cat = determine_category(p["name"])
        if old_cat != new_cat:
            p["category"] = new_cat
            count_changed += 1
            
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[{os.path.basename(file_path)}] Reclassified {count_changed} products to accurate categories!")

# Run bundle generator to inline the clean data into index.html
import build_full_bundle
build_full_bundle.bundle()
print("[BUNDLE] Re-bundled clean data into index.html!")
