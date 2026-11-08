import urllib.request
import urllib.parse
import json
import re

def search_11st_images(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    }
    url = f"https://m.11st.co.kr/MW/Search/searchDetail.tmall?kwd={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        imgs = re.findall(r'https?://[^\s"\'<>]+?\.(?:jpg|png|jpeg)', html, re.IGNORECASE)
        clean = []
        for img in imgs:
            if "cdn.011st.com" in img or "image.11st.co.kr" in img:
                if img not in clean and not any(x in img for x in ['logo', 'banner', 'btn', 'icon', 'bg']):
                    clean.append(img)
        return clean
    except Exception as e:
        print(f"11st error for {query}: {e}")
        return []

if __name__ == "__main__":
    products = [
        "코카콜라 500ml", "광동 비타500 100ml", "농심 신라면 컵 65g", "CJ 햇반 210g",
        "빙그레 바나나맛우유 240ml", "하겐다즈 파인트 바닐라 473ml", "오리온 포카칩 오리지널 66g"
    ]
    for p in products:
        imgs = search_11st_images(p)
        print(f"[{p}] 11st images count: {len(imgs)}")
        for img in imgs[:2]:
            print("  ->", img)
