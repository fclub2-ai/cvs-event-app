import urllib.request
import urllib.parse
import json
import re

def get_ssg_image(product_name):
    url = f"https://www.ssg.com/search.ssg?query={urllib.parse.quote(product_name)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        # SSG images: sitem.ssgcdn.com or item.ssgcdn.com
        imgs = re.findall(r'https?://(?:sitem|item)\.ssgcdn\.com/[^"\'\s<>]+\.(?:jpg|jpeg|png)', html, re.IGNORECASE)
        clean = []
        for img in imgs:
            if not any(x in img for x in ['logo', 'banner', 'icon', 'bg', 'event']):
                clean.append(img)
        return clean
    except Exception as e:
        print(f"SSG error for {product_name}: {e}")
        return []

def get_gmarket_image(product_name):
    url = f"https://browse.gmarket.co.kr/search?keyword={urllib.parse.quote(product_name)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        imgs = re.findall(r'https?://gdimg\.gmarket\.co\.kr/[^"\'\s<>]+\.(?:jpg|jpeg|png)', html, re.IGNORECASE)
        clean = []
        for img in imgs:
            if img not in clean:
                clean.append(img)
        return clean
    except Exception as e:
        print(f"Gmarket error for {product_name}: {e}")
        return []

if __name__ == "__main__":
    products = [
        "코카콜라 500ml", "광동 비타500 100ml", "몬스터에너지 355ml", "농심 신라면 컵 65g",
        "CJ 햇반 210g", "빙그레 바나나맛우유 240ml", "하겐다즈 파인트 바닐라 473ml", "오리온 포카칩 오리지널 66g"
    ]
    for p in products:
        ssg_imgs = get_ssg_image(p)
        gm_imgs = get_gmarket_image(p)
        print(f"[{p}] SSG: {len(ssg_imgs)} imgs, Gmarket: {len(gm_imgs)} imgs")
        if ssg_imgs:
            print("  SSG ->", ssg_imgs[0])
        if gm_imgs:
            print("  Gmarket ->", gm_imgs[0])
