import sys, json
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('backend/cvs_data.json', encoding='utf-8'))
print('Total products:', len(d['products']))
print('Total stores:', len(d.get('stores', [])))

# Brand distribution
brands = {}
for p in d['products']:
    brands[p['brand']] = brands.get(p['brand'], 0) + 1
print('Brands:', brands)

# Check for screenshot products
print('\n--- 스크린샷에 나온 상품명 검색 ---')
keywords = ['코카콜라', '코카', '새콤달콤', '크라운', '오렉바', '광동', '비타500']
for kw in keywords:
    matches = [p for p in d['products'] if kw in p['name']]
    if matches:
        print(f'\n[{kw}] {len(matches)}건:')
        for m in matches[:3]:
            print(f'  [{m["brand"]}] {m["name"]} => {m["image"]}')

# The website shows "CU 크라운)새콤달콤복숭아" with Coca-Cola image
# Let's check what the website ACTUALLY displays vs what's in DB
print('\n--- 웹사이트 표시 상품명으로 검색 ---')
web_names = [
    "크라운)새콤달콤복숭아",
    "PB)오렉바레모네이드맛",
    "광동 비타500 100ml",
    "농심 육개장 사발면",
    "맥스웰하우스 캔커피",
    "농심 멘토스 푸르티",
]
for wn in web_names:
    # Try partial match
    clean_wn = wn.replace(")", "").replace(" ", "")
    found = False
    for p in d['products']:
        clean_pn = p['name'].replace(")", "").replace(" ", "")
        if clean_wn in clean_pn or clean_pn in clean_wn:
            print(f'  Found: [{p["brand"]}] {p["name"]}')
            print(f'    image: {p["image"]}')
            found = True
            break
    if not found:
        # More fuzzy
        parts = [c for c in wn.split(")") if c]
        for part in parts:
            for p in d['products']:
                if part.replace(" ", "") in p['name'].replace(" ", ""):
                    print(f'  Fuzzy found [{part}]: [{p["brand"]}] {p["name"]}')
                    print(f'    image: {p["image"]}')
                    found = True
                    break
            if found:
                break
    if not found:
        print(f'  NOT FOUND: {wn}')

# Check the actual image URL that shows Coca-Cola
# From screenshot, the Coca-Cola image looks like a naverncp URL
# Let's check what URL corresponds to Coca-Cola cans
print('\n--- naverncp URL 패턴 분석 ---')
naverncp_count = 0
woodongs_count = 0
emart_count = 0
seven_count = 0
other_count = 0
for p in d['products']:
    img = p.get('image', '')
    if 'naverncp.com' in img:
        naverncp_count += 1
    elif 'woodongs.com' in img:
        woodongs_count += 1
    elif 'emart24' in img:
        emart_count += 1
    elif '7-eleven' in img:
        seven_count += 1
    else:
        other_count += 1

print(f'  naverncp.com: {naverncp_count}')
print(f'  woodongs.com: {woodongs_count}')
print(f'  emart24.co.kr: {emart_count}')
print(f'  7-eleven.co.kr: {seven_count}')
print(f'  other: {other_count}')
