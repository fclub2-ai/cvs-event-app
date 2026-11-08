import urllib.request
import urllib.parse
import http.cookiejar
import json

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://gs25.gsretail.com/gscvs/ko/products/event-goods"
}

# 1. Visit main page to get cookies
req1 = urllib.request.Request("https://gs25.gsretail.com/gscvs/ko/products/event-goods", headers=headers)
opener.open(req1)

# 2. Call AJAX endpoint
url = "https://gs25.gsretail.com/gscvs/ko/products/event-goods-search?pageNum=1&pageSize=40&searchDeniedFlg=N"
data = urllib.parse.urlencode({
    "pageNum": "1",
    "pageSize": "40",
    "searchDeniedFlg": "N"
}).encode("utf-8")

req2 = urllib.request.Request(url, data=data, headers=headers)
try:
    res = opener.open(req2).read().decode("utf-8")
    data = json.loads(res)
    results = data.get("results", [])
    print(f"GS25 Success! Found {len(results)} items!")
    if results:
        print("Sample:", results[0].get("goodsNm"))
except Exception as e:
    print("Error:", e)
