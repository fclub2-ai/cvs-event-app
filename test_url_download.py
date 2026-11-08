import urllib.request

test_urls = [
    "https://static.megamart.com/product/image/1357/13572655/13572655_1_960.jpg",
    "https://img.danawa.com/prod_img/500000/775/811/img/6811775_1.jpg",
    "https://img.danawa.com/prod_img/500000/577/811/img/6811577_1.jpg"
]

for u in test_urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=10).read()
        print(f"URL {u[:60]}... => SUCCESS ({len(data)} bytes)")
    except Exception as e:
        print(f"URL {u[:60]}... => FAILED: {e}")
