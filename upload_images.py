import os
import json
import urllib.request
import urllib.parse
import re
import base64
import ssl
import sys

IMGBB_API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

PRODUCTS = [
    {"name": "나뚜루 파인트 녹차 474ml", "keywords": ["나뚜루", "녹차"], "query": "나뚜루 파인트 녹차 474ml 상품 이미지"},
    {"name": "롯데 월드콘 바닐라 160ml", "keywords": ["월드콘", "바닐라"], "query": "롯데 월드콘 바닐라 160ml 상품 이미지"},
    {"name": "빙그레 메로나 70ml", "keywords": ["메로나"], "query": "빙그레 메로나 70ml 상품 이미지"},
    {"name": "오리온 포카칩 오리지널 66g", "keywords": ["포카칩", "오리지널"], "query": "오리온 포카칩 오리지널 66g 상품 이미지"},
    {"name": "오리온 꼬북칩 콘스프맛 80g", "keywords": ["꼬북칩", "콘스프"], "query": "오리온 꼬북칩 콘스프맛 80g 상품 이미지"},
    {"name": "해태 허니버터칩 60g", "keywords": ["허니버터칩"], "query": "해태 허니버터칩 60g 상품 이미지"},
    {"name": "농심 새우깡 90g", "keywords": ["새우깡"], "query": "농심 새우깡 90g 상품 이미지"},
    {"name": "오리온 초코송이 50g", "keywords": ["초코송이"], "query": "오리온 초코송이 50g 상품 이미지"},
    {"name": "롯데 빼빼로 아몬드 37g", "keywords": ["빼빼로", "아몬드"], "query": "롯데 빼빼로 아몬드 37g 상품 이미지"},
    {"name": "롯데 가나 딥밀크 초콜릿 70g", "keywords": ["가나", "딥밀크"], "query": "롯데 가나 딥밀크 초콜릿 70g 상품 이미지"},
    {"name": "페레로로쉐 T3 37.5g", "keywords": ["페레로", "T3"], "query": "페레로로쉐 T3 37.5g 상품 이미지"},
    {"name": "하리보 골드베렌 곰젤리 100g", "keywords": ["하리보", "골드베렌"], "query": "하리보 골드베렌 곰젤리 100g 상품 이미지"},
    {"name": "오리온 초코파이 12입 팩", "keywords": ["초코파이"], "query": "오리온 초코파이 12입 상품 이미지"},
    {"name": "롯데 칙촉 120g", "keywords": ["칙촉"], "query": "롯데 칙촉 120g 상품 이미지"},
    {"name": "크리넥스 수프림소프트 30롤", "keywords": ["크리넥스", "수프림소프트"], "query": "크리넥스 수프림소프트 30롤 상품 이미지"},
    {"name": "리스테린 쿨민트 구강청결제 750ml", "keywords": ["리스테린", "쿨민트"], "query": "리스테린 쿨민트 구강청결제 750ml 상품 이미지"},
    {"name": "가그린 제로 구강청결제 750ml", "keywords": ["가그린", "제로"], "query": "가그린 제로 구강청결제 750ml 상품 이미지"},
    {"name": "페브리즈 깨끗한향 370ml", "keywords": ["페브리즈", "깨끗한향"], "query": "페브리즈 깨끗한향 370ml 상품 이미지"},
    {"name": "다우니 아로마보라 섬유유연제 1L", "keywords": ["다우니", "아로마보라"], "query": "다우니 아로마보라 섬유유연제 1L 상품 이미지"},
    {"name": "컨디션 스틱 헛개 18g", "keywords": ["컨디션", "스틱"], "query": "컨디션 스틱 헛개 18g 상품 이미지"},
    {"name": "여명808 숙취해소음료 140ml", "keywords": ["여명808"], "query": "여명808 숙취해소음료 140ml 상품 이미지"}
]

DATA_FILES = [
    r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json",
    r"C:\Users\fclub\cvs-event-app\cvs_data.json"
]

def search_image_url(query):
    # Search Naver Image Search HTML for real product packaging photos
    try:
        url = "https://search.naver.com/search.naver?where=image&query=" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'https://search\.pstatic\.net/common/\?src=[^"\s&]+', html)
            if not matches:
                matches = re.findall(r'https://search\.pstatic\.net/[^"\s&]+', html)
            if matches:
                return matches[0]
    except Exception as e:
        print(f"[SEARCH ERROR] {query}: {e}")
    return None

def download_image(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return resp.read()
    except Exception as e:
        print(f"[DOWNLOAD ERROR] {url}: {e}")
    return None

def upload_to_imgbb(img_bytes):
    try:
        b64 = base64.b64encode(img_bytes).decode('utf-8')
        post_data = urllib.parse.urlencode({
            'key': IMGBB_API_KEY,
            'image': b64
        }).encode('utf-8')
        req = urllib.request.Request("https://api.imgbb.com/1/upload", data=post_data, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('success'):
                return data['data']['url']
            else:
                print(f"[IMGBB API ERROR]: {data}")
    except Exception as e:
        print(f"[UPLOAD ERROR]: {e}")
    return None

def process():
    summary = {}
    print(f"Starting ImgBB processing for {len(PRODUCTS)} products...")

    for prod in PRODUCTS:
        name = prod['name']
        query = prod['query']
        print(f"\nProcessing product: {name}")

        img_src_url = search_image_url(query)
        if not img_src_url:
            print(f"Failed to find search image URL for {name}")
            continue

        print(f"Found source image: {img_src_url[:60]}...")
        img_bytes = download_image(img_src_url)
        if not img_bytes:
            print(f"Failed to download image bytes for {name}")
            continue

        print(f"Downloaded {len(img_bytes)} bytes. Uploading to ImgBB...")
        imgbb_url = upload_to_imgbb(img_bytes)
        if imgbb_url:
            print(f"SUCCESS: {name} -> {imgbb_url}")
            summary[name] = {
                "imgbb_url": imgbb_url,
                "keywords": prod['keywords']
            }
        else:
            print(f"FAILED to upload {name} to ImgBB")

    print("\n================ SUMMARY ================")
    for k, v in summary.items():
        print(f"{k}: {v['imgbb_url']}")

    # Save summary report
    with open(r"C:\Users\fclub\cvs-event-app\imgbb_summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # Update data files
    for filepath in DATA_FILES:
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        updated_count = 0
        for p in data.get('products', []):
            p_name = p.get('name', '')
            for target_name, res in summary.items():
                if all(kw in p_name for kw in res['keywords']):
                    p['image'] = res['imgbb_url']
                    updated_count += 1
                    break

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {updated_count} entries in {filepath}")

if __name__ == "__main__":
    process()
