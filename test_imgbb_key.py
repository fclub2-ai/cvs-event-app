"""
Step 1: ImgBB API Key 테스트
"""
import urllib.request
import urllib.parse
import base64
import json

IMGBB_API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

# 테스트: 작은 이미지 다운로드 후 ImgBB 업로드
test_url = "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=80&q=50"
req = urllib.request.Request(test_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    img_bytes = resp.read()

print(f"Downloaded test image: {len(img_bytes)} bytes")

b64 = base64.b64encode(img_bytes).decode("utf-8")
payload = urllib.parse.urlencode({
    "key": IMGBB_API_KEY,
    "image": b64,
    "name": "api_key_test",
}).encode("utf-8")

req2 = urllib.request.Request("https://api.imgbb.com/1/upload", data=payload, method="POST")
req2.add_header("Content-Type", "application/x-www-form-urlencoded")

with urllib.request.urlopen(req2, timeout=30) as resp2:
    result = json.loads(resp2.read().decode("utf-8"))

if result.get("success"):
    print(f"[OK] ImgBB API Key VALID!")
    print(f"Uploaded URL: {result['data']['url']}")
    print(f"Display URL: {result['data']['display_url']}")
else:
    print(f"[FAIL] {result}")
