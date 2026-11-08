import urllib.request
import urllib.parse
import json
import base64

API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"
url = "https://view01.wemep.co.kr/wmp-product/1/956/824969561/824969561.jpg"

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
data = urllib.request.urlopen(req, timeout=10).read()
print(f"Downloaded image size: {len(data)} bytes")

b64_data = base64.b64encode(data).decode("utf-8")
post_data = urllib.parse.urlencode({
    "key": API_KEY,
    "image": b64_data,
    "name": "vita500_official_wemakeprice"
}).encode("utf-8")

post_req = urllib.request.Request(
    "https://api.imgbb.com/1/upload",
    data=post_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
res = urllib.request.urlopen(post_req).read().decode("utf-8")
res_json = json.loads(res)
print("Uploaded ImgBB URL:", res_json["data"]["url"])
