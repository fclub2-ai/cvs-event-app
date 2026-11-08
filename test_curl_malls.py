import subprocess
import re
import urllib.parse

def test_mall_search(url, pattern):
    cmd = [
        "curl.exe", "-s", "-L",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    matches = re.findall(pattern, res.stdout, re.IGNORECASE)
    clean = list(dict.fromkeys(matches))
    return clean

if __name__ == "__main__":
    q = urllib.parse.quote("코카콜라 500ml")
    
    danawa_url = f"https://search.danawa.com/dsearch.php?query={q}"
    danawa_imgs = test_mall_search(danawa_url, r'https?://img\.danawa\.com/prod_img/[^"\'\s<>]+\.(?:jpg|png)')
    print("Danawa images found:", len(danawa_imgs))
    for img in danawa_imgs[:3]:
        print("  ->", img)

    lotte_url = f"https://www.lotteon.com/search/search/search.ec?render=search&q={q}"
    lotte_imgs = test_mall_search(lotte_url, r'https?://cdn\.lotteon\.com/[^"\'\s<>]+\.(?:jpg|png)')
    print("Lotte ON images found:", len(lotte_imgs))
    for img in lotte_imgs[:3]:
        print("  ->", img)
