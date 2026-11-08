import subprocess
import re
import urllib.parse
import json

def get_official_store_package_image(product_name):
    query = f"{product_name} 1개 공식 상품 포장"
    encoded = urllib.parse.quote(query)
    url = f"https://m.search.naver.com/search.naver?where=m_image&query={encoded}"
    cmd = [
        "curl.exe", "-s", "-L",
        "-H", "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    html = res.stdout
    imgs = re.findall(r'https://search\.pstatic\.net/[^"\'\s<>\\]+', html)
    
    official_store_cdns = [
        'shop1.phinf.naver.net',
        'shop-phinf.pstatic.net',
        'megamart.com',
        'momq.co.kr',
        'ssgcdn.com',
        'lotteon.com',
        'coupangcdn.com',
        '011st.com',
        'gmarket.co.kr',
        'auction.co.kr',
        'emart24.co.kr',
        'bgfretail.com'
    ]
    
    filtered_urls = []
    for img in imgs:
        decoded = urllib.parse.unquote(img)
        if any(cdn in decoded for cdn in official_store_cdns):
            if not any(x in decoded for x in ['blog', 'cafe', 'kin', 'type=f', 'logo', 'icon']):
                filtered_urls.append(decoded)
                
    return filtered_urls

if __name__ == "__main__":
    products = [
        "광동 비타500 100ml", "코카콜라 500ml", "칠성사이다 500ml", "몬스터에너지 355ml",
        "맥스웰하우스 캔커피 175ml", "농심 신라면 컵 65g", "CJ 햇반 210g", "빙그레 바나나맛우유 240ml",
        "연세우유 생크림빵 130g", "하겐다즈 파인트 바닐라 473ml", "해태 허니버ter칩 60g"
    ]
    for p in products:
        urls = get_official_store_package_image(p)
        print(f"[{p}] Official Store Images: {len(urls)}")
        for u in urls[:2]:
            print("  ->", u)
