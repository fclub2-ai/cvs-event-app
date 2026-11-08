import urllib.request
import urllib.parse
import json
import re

def search_image(product_name):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(product_name + " 상품 이미지")
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        matches = re.findall(r'//external-content\.duckduckgo\.com/iu/\?u=(https%3A%2F%2F[^&"\']+)', html)
        valid_urls = []
        for m in matches:
            decoded = urllib.parse.unquote(m)
            if any(ext in decoded.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                valid_urls.append(decoded)
        return valid_urls
    except Exception as e:
        print(f"Error searching {product_name}: {e}")
        return []

if __name__ == "__main__":
    test_products = ["코카콜라 500ml", "광동 비타500 100ml", "몬스터에너지 355ml", "농심 신라면 컵 65g"]
    for p in test_products:
        urls = search_image(p)
        print(f"=== {p} ===")
        for u in urls[:3]:
            print("  -", u)
