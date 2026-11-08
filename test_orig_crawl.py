import subprocess
import re
import urllib.parse
import json

def get_official_image_via_naver_shopping(product_name):
    # Search specifically on official shopping stores (SSG, LotteON, 11st, Homeplus, Coupang official)
    encoded = urllib.parse.quote(f"{product_name} 공식")
    url = f"https://m.search.naver.com/search.naver?where=m_image&query={encoded}"
    cmd = [
        "curl.exe", "-s", "-L",
        "-H", "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    html = res.stdout
    imgs = re.findall(r'https://search\.pstatic\.net/[^"\'\s<>\\]+', html)
    
    clean_urls = []
    for img in imgs:
        decoded = urllib.parse.unquote(img)
        # We want the original source URL inside src=...
        src_match = re.search(r'src=(https?%3A%2F%2F[^&"\']+)', img)
        if src_match:
            orig = urllib.parse.unquote(src_match.group(1))
            if any(ext in orig.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                if not any(x in orig for x in ['blog', 'cafe', 'kin', 'thumb']):
                    clean_urls.append(orig)
    return clean_urls

if __name__ == "__main__":
    p = "광동 비타500 100ml"
    urls = get_official_image_via_naver_shopping(p)
    print(f"[{p}] Found original image sources:")
    for u in urls[:5]:
        print("  ->", u)
