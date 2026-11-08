import subprocess
import re
import urllib.parse

def fetch_naver_shopping_images(query):
    encoded = urllib.parse.quote(query)
    url = f"https://search.shopping.naver.com/search/all?query={encoded}"
    cmd = [
        "curl.exe", "-s", "-L",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "-H", "Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    html = res.stdout
    imgs = re.findall(r'https://shopping-phinf\.pstatic\.net/[^"?\s\'\\]+', html)
    clean = []
    for img in imgs:
        img_clean = re.sub(r'\?.*$', '', img)
        if img_clean not in clean and not any(x in img_clean for x in ['logo', 'banner', 'icon']):
            clean.append(img_clean)
    return clean

if __name__ == "__main__":
    products = ["코카콜라 500ml", "광동 비타500 100ml", "몬스터에너지 355ml", "농심 신라면 컵 65g", "CJ 햇반 210g"]
    for p in products:
        imgs = fetch_naver_shopping_images(p)
        print(f"[{p}] found {len(imgs)} Naver images")
        for img in imgs[:2]:
            print("  ->", img)
