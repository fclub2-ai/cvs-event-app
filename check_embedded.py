import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

html = open('index.html', encoding='utf-8').read()
print(f'index.html size: {len(html)} bytes')

# Extract embedded data
m = re.search(r'window\.EMBEDDED_CVS_DATA\s*=\s*(\{.*?\});', html, re.DOTALL)
if not m:
    print('NO EMBEDDED DATA FOUND in index.html!')
else:
    d = json.loads(m.group(1))
    prods = d.get('products', [])
    print(f'Embedded products: {len(prods)}')
    
    # Show first 5
    print('\nFirst 5 embedded products:')
    for p in prods[:5]:
        print(f'  [{p["brand"]}] {p["name"]} => {p["image"]}')
    
    # Check the screenshot products
    print('\n--- 스크린샷 상품 검색 (embedded data) ---')
    for kw in ['새콤달콤', '비타500', '육개장', '멘토스', '코카콜라']:
        matches = [p for p in prods if kw in p['name']]
        print(f'\n[{kw}] {len(matches)}건:')
        for m2 in matches[:3]:
            print(f'  [{m2["brand"]}] {m2["name"]} => {m2["image"]}')
    
    # Check if old-format names exist (e.g. "GS25) 광동 비타500 100ml")
    print('\n--- 옛날 상품명 형식 검색 ---')
    old_names = [p for p in prods if p['name'].startswith('GS25)') or p['name'].startswith('CU)')]
    print(f'Old-format names (starting with brand prefix): {len(old_names)}')
    for p in old_names[:5]:
        print(f'  [{p["brand"]}] {p["name"]} => {p["image"]}')
