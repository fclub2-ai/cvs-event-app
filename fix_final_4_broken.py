import urllib.request
import urllib.parse
import json
import base64
import subprocess
import re

API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

BROKEN_4_ITEMS = [
    "삼다수 2.0L",
    "오리온 초코송이 50g",
    "롯데 빼빼로 아몬드 37g",
    "다우니 아로마보라 섬유유연제 1L"
]

def harvest_real_product_image(product_name):
    query = f"{product_name} 누끼 상품 이미지"
    encoded = urllib.parse.quote(query)
    url = f"https://m.search.naver.com/search.naver?where=m_image&query={encoded}"
    cmd = [
        "curl.exe", "-s", "-L",
        "-H", "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        html = res.stdout
        imgs = re.findall(r'https://search\.pstatic\.net/[^"\'\s<>\\]+', html)
        
        shopping_imgs = []
        other_imgs = []
        for img in imgs:
            decoded = urllib.parse.unquote(img)
            if any(cdn in decoded for cdn in ['lotteon.com', 'ssgcdn.com', 'coupangcdn.com', '011st.com', 'shop1.phinf.naver.net', 'shop-phinf.pstatic.net', 'wemep.co.kr', 'gmarket.co.kr', 'homeplus.co.kr', 'enuri.com']):
                shopping_imgs.append(decoded)
            elif not any(x in decoded for x in ['blogpfthumb', 'type=f', 'logo', 'icon']):
                other_imgs.append(decoded)
                
        candidates = shopping_imgs + other_imgs
        for candidate in candidates[:5]:
            try:
                req = urllib.request.Request(candidate, headers={"User-Agent": "Mozilla/5.0"})
                img_bytes = urllib.request.urlopen(req, timeout=8).read()
                if len(img_bytes) > 2000:
                    return img_bytes
            except Exception:
                continue
    except Exception as e:
        print(f"Scrape error for {product_name}: {e}")
    return None

def upload_b64_to_imgbb(img_bytes, filename):
    try:
        b64_data = base64.b64encode(img_bytes).decode("utf-8")
        post_data = urllib.parse.urlencode({
            "key": API_KEY,
            "image": b64_data,
            "name": filename
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.imgbb.com/1/upload",
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        res = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
        res_json = json.loads(res)
        if res_json.get("success"):
            return res_json["data"]["url"]
    except Exception as e:
        print(f"ImgBB upload error for {filename}: {e}")
    return None

def run_fix_4():
    fixed = {}
    print(f"Fixing final {len(BROKEN_4_ITEMS)} broken items...")
    for p in BROKEN_4_ITEMS:
        print(f"Processing: {p}")
        img_bytes = harvest_real_product_image(p)
        if img_bytes:
            url = upload_b64_to_imgbb(img_bytes, p)
            if url:
                fixed[p] = url
                print(f"  -> FIXED ImgBB URL: {url}")
            else:
                print("  -> Upload failed")
        else:
            print("  -> Harvest failed")

    # Update data files
    for data_path in ["cvs_data.json", "backend/cvs_data.json"]:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        products = data.get("products", data) if isinstance(data, dict) else data
        for prod in products:
            name = prod["name"]
            base_name = name.split(") ")[-1] if ") " in name else name
            if base_name in fixed:
                prod["image"] = fixed[base_name]
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild bundle
    subprocess.run(["python", "build_full_bundle.py"])
    print("Complete!")

if __name__ == "__main__":
    run_fix_4()
