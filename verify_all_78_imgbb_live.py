import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

with open("cvs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", data) if isinstance(data, dict) else data

base_map = {}
for p in products:
    name = p["name"]
    base_name = name.split(") ")[-1] if ") " in name else name
    img = p.get("image", "")
    if base_name not in base_map:
        base_map[base_name] = img

def check_single_url(item):
    name, img_url = item
    if not img_url or "i.ibb.co" not in img_url:
        return (name, img_url, False, "No ImgBB URL")
    try:
        req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req, timeout=5)
        body = res.read()
        if res.status == 200 and len(body) > 1000:
            return (name, img_url, True, f"OK ({len(body)} bytes)")
        else:
            return (name, img_url, False, f"Status {res.status}, size {len(body)} bytes")
    except Exception as e:
        return (name, img_url, False, str(e))

if __name__ == "__main__":
    print(f"Auditing live image status for {len(base_map)} products in parallel...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_single_url, base_map.items()))

    valid = [r for r in results if r[2]]
    broken = [r for r in results if not r[2]]

    print(f"\n=== AUDIT RESULTS ===")
    print(f"[VALID] Working product images: {len(valid)} / {len(base_map)}")
    print(f"[BROKEN] Broken/Missing product images: {len(broken)} / {len(base_map)}")

    if broken:
        print("\n--- BROKEN ITEMS LIST ---")
        for idx, (name, img_url, _, err) in enumerate(broken, 1):
            print(f"{idx:02d}. {name} => {err}")

    with open("broken_items_audit.json", "w", encoding="utf-8") as f:
        json.dump([{"name": b[0], "url": b[1], "reason": b[3]} for b in broken], f, ensure_ascii=False, indent=2)
