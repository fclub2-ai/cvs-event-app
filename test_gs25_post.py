import urllib.request
import urllib.parse
import json
import re

url = "https://gs25.gsretail.com/gscvs/ko/products/event-goods-search?pageNum=1&pageSize=40&searchDeniedFlg=N"
data = urllib.parse.urlencode({
    "pageNum": "1",
    "pageSize": "40",
    "searchDeniedFlg": "N",
    "eventControlCode": "1,2" # 1+1, 2+1
}).encode("utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://gs25.gsretail.com/gscvs/ko/products/event-goods",
    "X-Requested-With": "XMLHttpRequest"
}

try:
    req = urllib.request.Request(url, data=data, headers=headers)
    res = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
    data = json.loads(res)
    print("GS25 Success! Total count:", len(data.get("results", [])))
    if data.get("results"):
        print("Sample:", data["results"][0].get("goodsNm"))
except Exception as e:
    print("Error:", e)
