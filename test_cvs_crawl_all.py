import subprocess
import re
import urllib.parse
import json

def search_product_package_image(product_name):
    # Search terms focused on exact product packaging, canned, bottled, boxed product
    query = f"{product_name} 상품 포장 이미지"
    url = f"https://m.search.naver.com/search.naver?where=m_image&query={urllib.parse.quote(query)}"
    cmd = [
        "curl.exe", "-s", "-L",
        "-H", "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    html = res.stdout
    
    # Extract raw pstatic.net images
    raw_imgs = re.findall(r'https://search\.pstatic\.net/[^"\'\s<>\\]+', html)
    
    valid_urls = []
    for img in raw_imgs:
        decoded = urllib.parse.unquote(img)
        # Avoid generic blog avatars, thumbnails, logos, buttons
        if not any(x in decoded for x in ['blogpfthumb', 'type=f', 'logo', 'icon', 'button', 'banner']):
            valid_urls.append(decoded)
            
    return valid_urls

if __name__ == "__main__":
    test_products = [
        "광동 비타500 100ml", "코카콜라 500ml", "몬스터에너지 355ml",
        "농심 신라면 컵 65g", "CJ 햇반 210g", "빙그레 바나나맛우유 240ml"
    ]
    for p in test_products:
        imgs = search_product_package_image(p)
        print(f"[{p}] Found {len(imgs)} candidate package images:")
        for img in imgs[:2]:
            print("  ->", img[:100])
