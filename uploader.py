import os
import json
import urllib.request
import urllib.parse
import re
import base64
import ssl

IMGBB_API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

TARGET_PRODUCTS = [
    {
        "name": "나뚜루 파인트 녹차 474ml",
        "keywords": ["나뚜루", "녹차"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzAzMjJfMjAy%2FMDAxNjc5NDk1NDkxNTU1.gL4YjB9-3Mh1l_x53qP67tYgX8g5X5.JPEG.sample%2Fnatuur.jpg"
    },
    {
        "name": "롯데 월드콘 바닐라 160ml",
        "keywords": ["월드콘", "바닐라"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fworldcone.jpg"
    },
    {
        "name": "빙그레 메로나 70ml",
        "keywords": ["메로나"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fmerona.jpg"
    },
    {
        "name": "오리온 포카칩 오리지널 66g",
        "keywords": ["포카칩", "오리지널"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fpocachip.jpg"
    },
    {
        "name": "오리온 꼬북칩 콘스프맛 80g",
        "keywords": ["꼬북칩", "콘스프"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fkkobuk.jpg"
    },
    {
        "name": "해태 허니버터칩 60g",
        "keywords": ["허니버터칩"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fhoneybutter.jpg"
    },
    {
        "name": "농심 새우깡 90g",
        "keywords": ["새우깡"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fsaewookkang.jpg"
    },
    {
        "name": "오리온 초코송이 50g",
        "keywords": ["초코송이"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fchocosongyi.jpg"
    },
    {
        "name": "롯데 빼빼로 아몬드 37g",
        "keywords": ["빼빼로", "아몬드"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fpepero.jpg"
    },
    {
        "name": "롯데 가나 딥밀크 초콜릿 70g",
        "keywords": ["가나", "딥밀크"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fghana.jpg"
    },
    {
        "name": "페레로로쉐 T3 37.5g",
        "keywords": ["페레로", "T3"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fferrero.jpg"
    },
    {
        "name": "하리보 골드베렌 곰젤리 100g",
        "keywords": ["하리보", "골드베렌"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fharibo.jpg"
    },
    {
        "name": "오리온 초코파이 12입 팩",
        "keywords": ["초코파이"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fchocopie.jpg"
    },
    {
        "name": "롯데 칙촉 120g",
        "keywords": ["칙촉"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fchicchoc.jpg"
    },
    {
        "name": "크리넥스 수프림소프트 30롤",
        "keywords": ["크리넥스", "수프림소프트"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fkleenex.jpg"
    },
    {
        "name": "리스테린 쿨민트 구강청결제 750ml",
        "keywords": ["리스테린", "쿨민트"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Flisterine.jpg"
    },
    {
        "name": "가그린 제로 구강청결제 750ml",
        "keywords": ["가그린", "제로"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fgarglin.jpg"
    },
    {
        "name": "페브리즈 깨끗한향 370ml",
        "keywords": ["페브리즈", "깨끗한향"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Ffebreze.jpg"
    },
    {
        "name": "다우니 아로마보라 섬유유연제 1L",
        "keywords": ["다우니", "아로마보라"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fdowny.jpg"
    },
    {
        "name": "컨디션 스틱 헛개 18g",
        "keywords": ["컨디션", "스틱"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fcondition.jpg"
    },
    {
        "name": "여명808 숙취해소음료 140ml",
        "keywords": ["여명808"],
        "fallback_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA1MTVfOTYg%2FMDAxNjIxMDUyNTA5MjE2.sample.JPEG%2Fyeomyeong.jpg"
    }
]

DATA_FILES = [
    r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json",
    r"C:\Users\fclub\cvs-event-app\cvs_data.json"
]

def search_naver_image(query):
    try:
        url = "https://search.naver.com/search.naver?where=image&query=" + urllib.parse.quote(query + " 상품 이미지")
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract search.pstatic.net URLs
            matches = re.findall(r'https://search\.pstatic\.net/common/\?src=[^"\s&]+', html)
            if not matches:
                matches = re.findall(r'https://search\.pstatic\.net/[^"\s&]+', html)
            if matches:
                return matches[0]
    except Exception as e:
        print(f"Error searching image for {query}: {e}")
    return None

def download_image(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            return resp.read()
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
    return None

def upload_to_imgbb(image_bytes):
    try:
        b64_data = base64.b64encode(image_bytes).decode('utf-8')
        post_data = urllib.parse.urlencode({
            'key': IMGBB_API_KEY,
            'image': b64_data
        }).encode('utf-8')
        
        req = urllib.request.Request("https://api.imgbb.com/1/upload", data=post_data, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            res_json = json.loads(resp.read().decode('utf-8'))
            if res_json.get('success'):
                return res_json['data']['url']
            else:
                print(f"ImgBB API error: {res_json}")
    except Exception as e:
        print(f"Error uploading to ImgBB: {e}")
    return None

def run():
    results = {}
    print("Processing 21 products...")
    
    for item in TARGET_PRODUCTS:
        p_name = item['name']
        print(f"\n--- Processing: {p_name} ---")
        
        img_url = search_naver_image(p_name)
        if not img_url:
            img_url = item['fallback_url']
            print(f"Using fallback URL for {p_name}")
        else:
            print(f"Found search image URL: {img_url}")
            
        img_bytes = download_image(img_url)
        if not img_bytes:
            print(f"Downloading failed for {img_url}, trying fallback...")
            img_bytes = download_image(item['fallback_url'])
            
        if not img_bytes:
            print(f"Failed to download image for {p_name}")
            continue
            
        imgbb_url = upload_to_imgbb(img_bytes)
        if imgbb_url:
            print(f"SUCCESS: Uploaded {p_name} -> ImgBB: {imgbb_url}")
            results[p_name] = {
                "imgbb_url": imgbb_url,
                "keywords": item['keywords']
            }
        else:
            print(f"FAILED to upload ImgBB for {p_name}")

    # Save results json
    with open(r"C:\Users\fclub\cvs-event-app\imgbb_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Update data files
    print("\nUpdating JSON data files...")
    for data_path in DATA_FILES:
        if not os.path.exists(data_path):
            continue
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        updated_count = 0
        for p in data.get('products', []):
            prod_name = p.get('name', '')
            for target_name, res in results.items():
                if all(kw in prod_name for kw in res['keywords']):
                    p['image'] = res['imgbb_url']
                    updated_count += 1
                    break
                    
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {updated_count} product images in {data_path}")

if __name__ == "__main__":
    main_run = run()
