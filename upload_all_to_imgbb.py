"""
CVS-Finder: 62개 미등록 상품의 실제 이미지를 네이버 쇼핑에서 검색 → 다운로드 → ImgBB 업로드
ImgBB API Key: c24ac8dace32780ff180b4b6e96cf4b0
"""

import json
import os
import re
import urllib.request
import urllib.parse
import base64
import time
import sys

IMGBB_API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "backend", "cvs_data.json")
ROOT_DATA_FILE = os.path.join(BASE_DIR, "cvs_data.json")


def download_image(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "image/*,*/*;q=0.8",
            "Referer": "https://search.shopping.naver.com/",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if len(data) > 500:
                return data
    except:
        pass
    return None


def upload_to_imgbb(image_bytes, name="product"):
    try:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = urllib.parse.urlencode({
            "key": IMGBB_API_KEY,
            "image": b64,
            "name": name[:30],
        }).encode("utf-8")
        req = urllib.request.Request(IMGBB_UPLOAD_URL, data=payload, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("success"):
                return result["data"]["display_url"]
    except Exception as e:
        print(f"    [IMGBB ERR] {e}")
    return None


def search_naver_product_image(query):
    """Search Naver Shopping for product image URL"""
    try:
        encoded = urllib.parse.quote(query)
        search_url = f"https://search.shopping.naver.com/search/all?query={encoded}&cat_id=&frm=NVSHATC"
        req = urllib.request.Request(search_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ko-KR,ko;q=0.9",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        
        # Extract product image URLs from Naver Shopping results
        # Pattern 1: shopping.phinf.naver.net thumbnails
        imgs = re.findall(r'(https?://shopping-phinf\.phinf\.naver\.net/[^"\'>\s]+)', html)
        if imgs:
            # Get highest quality version
            img_url = imgs[0].split("?")[0]
            return img_url
        
        # Pattern 2: Any product image
        imgs2 = re.findall(r'(https?://[^"\'>\s]*(?:product|goods|item)[^"\'>\s]*\.(?:jpg|png|webp))', html, re.IGNORECASE)
        if imgs2:
            return imgs2[0]
            
    except Exception as e:
        pass
    return None


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])

    # Group by base product name
    unique_bases = {}
    for p in products:
        name = p["name"]
        base = re.sub(r'^(GS25|CU|7-ELEVEN|EMART24)\)\s*', '', name)
        if base not in unique_bases:
            unique_bases[base] = []
        unique_bases[base].append(p)

    # Process only products that DON'T have ImgBB URLs
    imgbb_cache = {}  # base_name -> imgbb_url
    uploaded = 0
    skipped = 0
    failed = 0

    print(f"=== Processing {len(unique_bases)} unique products ===\n")

    for i, (base, variants) in enumerate(unique_bases.items()):
        # Skip if already on ImgBB
        if any("ibb.co" in v.get("image", "") for v in variants):
            skipped += 1
            # Ensure ALL variants use the same ImgBB URL
            imgbb_url = next(v["image"] for v in variants if "ibb.co" in v.get("image", ""))
            for v in variants:
                v["image"] = imgbb_url
            continue

        print(f"[{i+1}/{len(unique_bases)}] {base}")

        # Search Naver Shopping for real product image
        search_query = base.replace(")", " ").strip()
        naver_img = search_naver_product_image(search_query)
        
        if naver_img:
            print(f"  Found: {naver_img[:80]}...")
            img_data = download_image(naver_img)
            if img_data:
                safe_name = re.sub(r'[^a-zA-Z0-9]', '_', base)[:25]
                imgbb_url = upload_to_imgbb(img_data, safe_name)
                if imgbb_url:
                    for v in variants:
                        v["image"] = imgbb_url
                    uploaded += 1
                    print(f"  -> ImgBB: {imgbb_url}")
                else:
                    failed += 1
                    print(f"  -> ImgBB upload FAILED")
            else:
                failed += 1
                print(f"  -> Download FAILED")
        else:
            # Fallback: try with simpler query
            simple_query = base.split()[-1] if len(base.split()) > 1 else base
            naver_img2 = search_naver_product_image(simple_query + " 편의점")
            if naver_img2:
                img_data = download_image(naver_img2)
                if img_data:
                    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', base)[:25]
                    imgbb_url = upload_to_imgbb(img_data, safe_name)
                    if imgbb_url:
                        for v in variants:
                            v["image"] = imgbb_url
                        uploaded += 1
                        print(f"  -> ImgBB (fallback): {imgbb_url}")
                    else:
                        failed += 1
                else:
                    failed += 1
            else:
                failed += 1
                print(f"  -> No image found")

        time.sleep(0.5)

    # Save
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(ROOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n=== COMPLETE ===")
    print(f"Uploaded to ImgBB: {uploaded}")
    print(f"Already on ImgBB: {skipped}")
    print(f"Failed: {failed}")
    print(f"Total unique: {len(unique_bases)}, Total products: {len(products)}")


if __name__ == "__main__":
    main()
