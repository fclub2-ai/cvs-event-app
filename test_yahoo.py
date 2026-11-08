import urllib.request
import urllib.parse
import json
import re

def search_yahoo_images(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    url = f"https://images.search.yahoo.com/search/images?p={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        # Yahoo images embeds imgurl=... in <img> tags or json
        matches = re.findall(r'imgurl=(https?%3A%2F%2F[^&"\']+)', html)
        clean = []
        for m in matches:
            decoded = urllib.parse.unquote(m)
            if any(ext in decoded.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                if decoded not in clean and not any(x in decoded for x in ['yimg.com', 'logo', 'icon']):
                    clean.append(decoded)
        return clean
    except Exception as e:
        print(f"Yahoo error for {query}: {e}")
        return []

if __name__ == "__main__":
    products = [
        "코카콜라 500ml", "광동 비타500 100ml", "몬스터에너지 355ml", "농심 신라면 컵 65g",
        "CJ 햇반 210g", "빙그레 바나나맛우유 240ml", "하겐다즈 파인트 바닐라 473ml", "오리온 포카칩 오리지널 66g"
    ]
    for p in products:
        imgs = search_yahoo_images(p + " 제품 사진")
        print(f"[{p}] Yahoo images count: {len(imgs)}")
        for img in imgs[:2]:
            print("  ->", img)
