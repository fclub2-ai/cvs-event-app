import urllib.request
import urllib.parse
import json
import re

def search_google_images(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch&hl=ko"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        # Extract full resolution images from Google's embedded JS array [\"http...\", height, width]
        matches = re.findall(r'\["(https?://[^"]+?\.(?:jpg|png|jpeg))",\s*\d+,\s*\d+\]', html, re.IGNORECASE)
        if not matches:
            matches = re.findall(r'https?://encrypted-tbn0\.gstatic\.com/images\?q=[^"\'\s&]+', html)
        clean = []
        for m in matches:
            if m not in clean:
                clean.append(m)
        return clean
    except Exception as e:
        print(f"Google error for {query}: {e}")
        return []

if __name__ == "__main__":
    products = [
        "코카콜라 500ml 페트", "광동 비타500 100ml 병", "농심 신라면 컵 65g", "CJ 햇반 210g"
    ]
    for p in products:
        imgs = search_google_images(p)
        print(f"[{p}] Google images count: {len(imgs)}")
        for img in imgs[:3]:
            print("  ->", img[:100])
