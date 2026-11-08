import json, sys
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json"
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

import re
unique = {}
for p in data["products"]:
    base = re.sub(r'^(GS25|CU|7-ELEVEN|EMART24)\)\s*', '', p["name"])
    if base not in unique:
        has_ibb = "ibb.co" in p.get("image","")
        unique[base] = {"cat": p["category"], "ibb": has_ibb}

need = [(k,v) for k,v in unique.items() if not v["ibb"]]
print(f"Need images: {len(need)}")
for i,(name,info) in enumerate(need):
    print(f"{i+1}. {name} [{info['cat']}]")
