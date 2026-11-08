import re
import json

INDEX_PATH = r"C:\Users\fclub\cvs-event-app\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r'window\.EMBEDDED_CVS_DATA\s*=\s*(\{.*?\});', html, flags=re.DOTALL)
if m:
    data = json.loads(m.group(1))
    products = data.get("products", [])
    print(f"Total embedded products: {len(products)}")
    for p in products:
        if "초코송이" in p["name"] or "맥스웰하우스" in p["name"]:
            print(f"Name: {p['name']} | Image: {p['image']}")
else:
    print("EMBEDDED_CVS_DATA not found!")
