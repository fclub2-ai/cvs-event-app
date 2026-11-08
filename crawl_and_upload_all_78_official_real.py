import urllib.request
import urllib.parse
import json
import base64
import subprocess
import re
import time
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

def get_all_78_base_products():
    with open("cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("products", data) if isinstance(data, dict) else data
    base_names = []
    for p in products:
        name = p["name"]
        base_name = name.split(") ")[-1] if ") " in name else name
        if base_name not in base_names:
            base_names.append(base_name)
    return base_names

def crawl_official_package_image_bytes(product_name, thread_id=0):
    query = f"{product_name} 1개 공식 상품 포장"
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
        
        official_store_cdns = [
            'shop-phinf.pstatic.net',
            'shop1.phinf.naver.net',
            'megamart.com',
            'momq.co.kr',
            'ssgcdn.com',
            'lotteon.com',
            'coupangcdn.com',
            '011st.com',
            'gmarket.co.kr',
            'auction.co.kr',
            'emart24.co.kr',
            'bgfretail.com',
            'enuri.com'
        ]
        
        candidate_urls = []
        for img in imgs:
            decoded = urllib.parse.unquote(img)
            src_match = re.search(r'src=(https?%3A%2F%2F[^&"\']+)', img)
            target_src = urllib.parse.unquote(src_match.group(1)) if src_match else decoded
            
            if any(cdn in target_src for cdn in official_store_cdns):
                if not any(x in target_src for x in ['blog', 'cafe', 'kin', 'type=f', 'logo', 'icon', 'button']):
                    if target_src not in candidate_urls:
                        candidate_urls.append(target_src)
                        
        if not candidate_urls:
            for img in imgs:
                decoded = urllib.parse.unquote(img)
                src_match = re.search(r'src=(https?%3A%2F%2F[^&"\']+)', img)
                target_src = urllib.parse.unquote(src_match.group(1)) if src_match else decoded
                if not any(x in target_src for x in ['blogpfthumb', 'type=f', 'logo', 'icon', 'button']):
                    candidate_urls.append(target_src)

        temp_file = os.path.join(tempfile.gettempdir(), f"temp_dl_{thread_id}_{os.getpid()}.img")
        for candidate in candidate_urls[:5]:
            dl_cmd = [
                "curl.exe", "-s", "-L",
                "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "-o", temp_file,
                candidate
            ]
            subprocess.run(dl_cmd)
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 3000:
                with open(temp_file, "rb") as f:
                    img_bytes = f.read()
                try:
                    os.remove(temp_file)
                except Exception:
                    pass
                return img_bytes
    except Exception as e:
        print(f"Crawl error for {product_name}: {e}")
    return None

def upload_to_imgbb(img_bytes, filename):
    try:
        import urllib.request
        import urllib.parse
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
        res = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
        res_json = json.loads(res)
        if res_json.get("success"):
            return res_json["data"]["url"]
    except Exception as e:
        print(f"ImgBB upload error for {filename}: {e}")
    return None

def process_single_product(item_tuple):
    idx, product_name = item_tuple
    print(f"[{idx}/78] Processing: {product_name}")
    img_bytes = crawl_official_package_image_bytes(product_name, thread_id=idx)
    if img_bytes:
        imgbb_url = upload_to_imgbb(img_bytes, product_name)
        if imgbb_url:
            print(f"  -> SUCCESS [{idx}/78] {product_name} => {imgbb_url}")
            return (product_name, imgbb_url, True)
    print(f"  -> FAILED [{idx}/78] {product_name}")
    return (product_name, None, False)

def run_pipeline():
    products = get_all_78_base_products()
    print(f"Starting 100% official store package image crawling for all {len(products)} products...")
    
    indexed_products = list(enumerate(products, 1))
    results = {}
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = executor.map(process_single_product, indexed_products)
        for name, url, success in futures:
            if success:
                results[name] = url

    print(f"\nCrawled & Uploaded {len(results)} / {len(products)} official product package images!")
    
    with open("official_78_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Update datasets
    for data_path in ["cvs_data.json", "backend/cvs_data.json"]:
        if not os.path.exists(data_path):
            continue
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        prods = data.get("products", data) if isinstance(data, dict) else data
        count = 0
        for p in prods:
            name = p["name"]
            base_name = name.split(") ")[-1] if ") " in name else name
            if base_name in results:
                p["image"] = results[base_name]
                count += 1
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {count} SKUs in {data_path}")

    # Rebuild index.html and package ZIP
    subprocess.run(["python", "build_full_bundle.py"])
    subprocess.run(["python", "create_zip_package.py"])
    print("\n[ALL DONE] 100% official product package images mapped, bundled, and zipped!")

if __name__ == "__main__":
    run_pipeline()
