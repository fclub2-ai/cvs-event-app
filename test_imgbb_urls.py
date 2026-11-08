import urllib.request

urls = [
    ("맥스웰하우스 캔커피", "https://i.ibb.co/1q6B0yP/8801037006018.jpg"),
    ("오리온 초코송이", "https://i.ibb.co/qN7X1vY/8801117134001.jpg"),
    ("농심 멘토스", "https://i.ibb.co/9kwJB7Qr/8990800000053.png"),
    ("광동 비타500", "https://i.ibb.co/6y4b2rP/8806004010173.jpg"),
]

for name, url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            print(f"[OK] {name}: Status {resp.status}, Size {len(resp.read())} bytes")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
