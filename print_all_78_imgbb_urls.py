import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json"
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

import re
unique_bases = {}
for p in data.get("products", []):
    base = re.sub(r'^(GS25|CU|7-ELEVEN|EMART24)\)\s*', '', p["name"])
    if base not in unique_bases:
        unique_bases[base] = p["image"]

for i, (base, img) in enumerate(unique_bases.items()):
    print(f"{i+1:02d}. {base} -> {img}")
