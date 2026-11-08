import json
import re

INDEX_PATH = r"C:\Users\fclub\cvs-event-app\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r'window\.EMBEDDED_CVS_DATA\s*=\s*(\{.*?\});', html, flags=re.DOTALL)
if m:
    data = json.loads(m.group(1))
    prods = data.get("products", [])
    print(f"Total embedded products in index.html: {len(prods)}")
    for p in prods:
        if "비타500" in p["name"]:
            print(f"ID: {p['id']}, Name: {p['name']}, Image: {p['image']}")
else:
    print("EMBEDDED_CVS_DATA not found in index.html")
