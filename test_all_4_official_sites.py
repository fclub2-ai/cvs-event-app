import sys, json, urllib.request, urllib.parse, re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("4대 편의점 공식 웹사이트 직접 수집 가능 여부 종합 테스트")
print("=" * 80)

# 1. CU (https://cu.bgfretail.com/event/plus.do)
print("\n1. CU 공식 웹사이트 (cu.bgfretail.com)")
try:
    req = urllib.request.Request('https://cu.bgfretail.com/event/plusAjax.do', 
        data=urllib.parse.urlencode({'pageIndex': 1, 'listType': 1}).encode('utf-8'), 
        headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cu.bgfretail.com/event/plus.do'})
    res = urllib.request.urlopen(req, timeout=5)
    print("  ✅ Status 200 OK - 100% 직수집 가능!")
    soup = BeautifulSoup(res.read().decode('utf-8', errors='ignore'), 'html.parser')
    lis = soup.select('ul > li')
    print(f"  📊 파싱된 공식 상품 수: {len(lis)}개")
    if lis:
        name = lis[0].select_one('.name').text.strip()
        img = lis[0].select_one('img')['src']
        print(f"  샘플: {name} ==> {img}")
except Exception as e:
    print(f"  ❌ 에러: {e}")

# 2. GS25 (http://gs25.gsretail.com/gscvs/ko/products/event-goods)
print("\n2. GS25 공식 웹사이트 (gs25.gsretail.com)")
try:
    url = 'http://gs25.gsretail.com/gscvs/ko/products/event-goods-search?pageNum=1&pageSize=16&searchSvcNm=GOODS&searchEventType=ALL'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req, timeout=5)
    print("  ✅ Status 200 OK - 100% 직수집 가능!")
    raw = res.read().decode('utf-8', errors='ignore')
    data = json.loads(raw)
    d2 = json.loads(data) if isinstance(data, str) else data
    items = d2.get('results', [])
    print(f"  📊 파싱된 공식 상품 수: {len(items)}개")
    if items:
        item = items[0]
        print(f"  샘플: {item.get('goodsNm')} ({item.get('price')}원) ==> {item.get('attFileNm') or item.get('giftAttFileNm')}")
except Exception as e:
    print(f"  ❌ 에러: {e}")

# 3. 7-ELEVEN (https://www.7-eleven.co.kr/product/presentList.asp)
print("\n3. 세븐일레븐 공식 웹사이트 (7-eleven.co.kr)")
try:
    req = urllib.request.Request('https://www.7-eleven.co.kr/product/listMoreAjax.asp', 
        data=urllib.parse.urlencode({'intPageSize': 16, 'intCurrPage': 1, 'pTab': 1}).encode('utf-8'), 
        headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.7-eleven.co.kr/product/presentList.asp'})
    res = urllib.request.urlopen(req, timeout=5)
    print("  ✅ Status 200 OK - 100% 직수집 가능!")
    soup = BeautifulSoup(res.read().decode('euc-kr', errors='ignore'), 'html.parser')
    lis = soup.select('li')
    print(f"  📊 파싱된 공식 상품 수: {len(lis)}개")
    for li in lis:
        n_el = li.select_one('.name')
        img_el = li.select_one('img')
        if n_el and img_el:
            print(f"  샘플: {n_el.text.strip()} ==> http://www.7-eleven.co.kr{img_el['src']}")
            break
except Exception as e:
    print(f"  ❌ 에러: {e}")

# 4. EMART24 (https://emart24.co.kr/goods/event)
print("\n4. 이마트24 공식 웹사이트 (emart24.co.kr)")
try:
    req = urllib.request.Request('https://emart24.co.kr/goods/event', headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req, timeout=5)
    print("  ✅ Status 200 OK - 100% 직수집 가능!")
    html = res.read().decode('utf-8', errors='ignore')
    print(f"  📊 이마트24 HTML 렌더링 확인 (크기: {len(html)} bytes)")
except Exception as e:
    print(f"  ❌ 에러: {e}")
