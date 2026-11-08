import urllib.request
import urllib.parse
import json
import re

def search_ddg_images_vqd(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    # Step 1: Get vqd token
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        vqd_match = re.search(r'vqd=([\d-]+)', html)
        if not vqd_match:
            vqd_match = re.search(r'vqd="([^"]+)"', html)
        if not vqd_match:
            print(f"No vqd for {query}")
            return []
        vqd = vqd_match.group(1)
        
        # Step 2: Query i.js
        img_url = f"https://duckduckgo.com/i.js?l=wt-wt&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,&p=1"
        req_img = urllib.request.Request(img_url, headers=headers)
        res = urllib.request.urlopen(req_img, timeout=10).read().decode("utf-8", errors="ignore")
        data = json.loads(res)
        results = data.get("results", [])
        return [r["image"] for r in results if "image" in r]
    except Exception as e:
        print(f"DDG API error for {query}: {e}")
        return []

if __name__ == "__main__":
    products = [
        "코카콜라 500ml", "광동 비타500 100ml", "농심 신라면 컵 65g", "CJ 햇반 210g",
        "빙그레 바나나맛우유 240ml", "하겐다즈 파인트 바닐라 473ml", "오리온 포카칩 오리지널 66g"
    ]
    for p in products:
        imgs = search_ddg_images_vqd(p + " 상품 사진")
        print(f"[{p}] DDG API images count: {len(imgs)}")
        for img in imgs[:2]:
            print("  ->", img)
