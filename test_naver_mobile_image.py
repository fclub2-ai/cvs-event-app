import subprocess
import re
import urllib.parse
import json

def search_naver_mobile_images(query):
    encoded = urllib.parse.quote(query + " 상품")
    url = f"https://m.search.naver.com/search.naver?where=m_image&query={encoded}"
    cmd = [
        "curl.exe", "-s", "-L",
        "-H", "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "-H", "Accept-Language: ko-KR,ko;q=0.9",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    html = res.stdout
    # Naver Mobile image search embeds original or thumbnail image URLs starting with https://search.pstatic.net/
    imgs = re.findall(r'https://search\.pstatic\.net/[^"\'\s<>\\]+', html)
    clean = []
    for img in imgs:
        # Unescape unicode or html entities if needed
        clean_img = urllib.parse.unquote(img)
        if clean_img not in clean and not any(x in clean_img for x in ['type=f', 'logo', 'icon', 'banner']):
            clean.append(clean_img)
    return clean

if __name__ == "__main__":
    products = [
        "코카콜라 500ml", "코카콜라 제로 500ml", "칠성사이다 500ml", "광동 비타500 100ml",
        "몬스터에너지 355ml", "핫식스 250ml", "농심 신라면 컵 65g", "CJ 햇반 210g",
        "서울우유 딸기우유 300ml", "연세우유 생크림빵 130g", "해태 허니버터칩 60g"
    ]
    for p in products:
        imgs = search_naver_mobile_images(p)
        print(f"[{p}] Naver Mobile images: {len(imgs)}")
        for img in imgs[:2]:
            print("  ->", img[:100])
