import urllib.request
import urllib.parse
import json
import re

def search_naver_shopping(product_name):
    query = product_name
    url = f"https://search.shopping.naver.com/search/all?query={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        # Naver shopping embeds product images like https://shopping-phinf.pstatic.net/...
        imgs = re.findall(r'https://shopping-phinf\.pstatic\.net/[^"?\s\']+', html)
        # Filter unique valid product image links (usually contain _160, _300, _500, or main image)
        clean_imgs = []
        for img in imgs:
            # Upgrade thumbnail size to full size by stripping resolution suffixes if needed
            clean_url = re.sub(r'\?type=.*$', '', img)
            if clean_url not in clean_imgs:
                clean_imgs.append(clean_url)
        return clean_imgs
    except Exception as e:
        print(f"Error fetching {product_name}: {e}")
        return []

if __name__ == "__main__":
    test_products = [
        "코카콜라 500ml", "칠성사이다 500ml", "광동 비타500 100ml", "몬스터에너지 355ml",
        "농심 신라면 컵 65g", "오뚜기 진라면 매운맛 컵", "CJ 햇반 210g", "빙그레 바나나맛우유 240ml",
        "연세우유 생크림빵", "하겐다즈 파인트 바닐라", "농심 새우깡 90g", "크리넥스 수프림소프트 30롤"
    ]
    for p in test_products:
        imgs = search_naver_shopping(p)
        print(f"[{p}] found {len(imgs)} Naver Shopping images:")
        for img in imgs[:2]:
            print("  ->", img)
