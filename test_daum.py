import urllib.request
import urllib.parse
import json
import re

def search_daum_shopping(product_name):
    query = product_name + " 공식 이미지"
    url = f"https://search.daum.net/search?w=img&q={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        # Daum image search returns img urls in original=... or fname=...
        matches = re.findall(r'fname=(https?%3A%2F%2F[^&"\']+)', html)
        if not matches:
            matches = re.findall(r'src="(https?://[^"]+?\.(?:jpg|jpeg|png|webp))"', html, re.IGNORECASE)
        clean = []
        for m in matches:
            decoded = urllib.parse.unquote(m)
            if "daumcdn.net" in decoded or "img1.daumcdn.net" in decoded:
                continue
            if any(ext in decoded.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                if decoded not in clean:
                    clean.append(decoded)
        return clean
    except Exception as e:
        print(f"Error for {product_name}: {e}")
        return []

if __name__ == "__main__":
    products = ["코카콜라 500ml", "광동 비타500 100ml", "농심 신라면 컵 65g", "CJ 햇반 210g"]
    for p in products:
        imgs = search_daum_shopping(p)
        print(f"[{p}] Daum images count: {len(imgs)}")
        for img in imgs[:3]:
            print("  ->", img)
