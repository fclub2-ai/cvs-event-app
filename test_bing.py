import urllib.request
import urllib.parse
import json
import re

def search_bing_images(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = "https://www.bing.com/images/search?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        # Bing embeds murl (media url) inside m="{...}" attributes
        matches = re.findall(r'murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png|webp))&quot;', html, re.IGNORECASE)
        if not matches:
            matches = re.findall(r'"murl":"(https?://[^"]+?\.(?:jpg|jpeg|png|webp))"', html, re.IGNORECASE)
        return list(dict.fromkeys(matches))
    except Exception as e:
        print(f"Bing search error for {query}: {e}")
        return []

if __name__ == "__main__":
    products = [
        "코카콜라 500ml", "코카콜라 제로 500ml", "칠성사이다 500ml", "광동 비타500 100ml",
        "몬스터에너지 355ml", "농심 신라면 컵 65g", "오뚜기 진라면 매운맛 컵", "CJ 햇반 210g"
    ]
    for p in products:
        imgs = search_bing_images(p + " 상품")
        print(f"[{p}] found {len(imgs)} images:")
        for img in imgs[:2]:
            print("  ->", img)
