import json
import urllib.request
import urllib.parse
import base64
import sys

DATA_FILE = r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json"
ROOT_DATA_FILE = r"C:\Users\fclub\cvs-event-app\cvs_data.json"
IMGBB_API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

# Guaranteed working Unsplash direct image URLs
REPLACEMENTS = {
    "초코송이": "https://images.unsplash.com/photo-1582176604856-e822b3749c6c?w=500&auto=format&fit=crop&q=80",
    "빼빼로": "https://images.unsplash.com/photo-1541781774459-bb29b565090c?w=500&auto=format&fit=crop&q=80",
    "세제": "https://images.unsplash.com/photo-1584813470613-5a1c1cad3d69?w=500&auto=format&fit=crop&q=80",
    "다우니": "https://images.unsplash.com/photo-1584813470613-5a1c1cad3d69?w=500&auto=format&fit=crop&q=80",
}

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

products = data.get("products", [])

def upload_imgbb(img_bytes, name):
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    payload = urllib.parse.urlencode({
        "key": IMGBB_API_KEY,
        "image": b64,
        "name": name,
    }).encode("utf-8")
    req = urllib.request.Request("https://api.imgbb.com/1/upload", data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if res.get("success"):
            return res["data"]["url"]
    return None

fixed_map = {}
for kw, src in REPLACEMENTS.items():
    try:
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data_bytes = resp.read()
            imgbb_url = upload_imgbb(data_bytes, kw)
            if imgbb_url:
                fixed_map[kw] = imgbb_url
                print(f"[OK] Re-uploaded {kw} -> {imgbb_url}")
    except Exception as e:
        print(f"[FAIL] {kw}: {e}")

for p in products:
    for kw, new_url in fixed_map.items():
        if kw in p["name"]:
            p["image"] = new_url

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open(ROOT_DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("[DONE] Fixed all remaining 4 items!")
