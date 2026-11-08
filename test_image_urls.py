import sys, json, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

# Test if the naverncp.com image URLs actually work (return HTTP 200)
d = json.load(open('backend/cvs_data.json', encoding='utf-8'))

test_urls = []
seen_domains = set()
for p in d['products']:
    img = p.get('image', '')
    # Extract domain
    if '://' in img:
        domain = img.split('://')[1].split('/')[0]
        if domain not in seen_domains:
            seen_domains.add(domain)
            test_urls.append((p['name'], p['brand'], img))
    if len(test_urls) >= 10:
        break

# Also add specific products
for p in d['products']:
    if '비타500' in p['name'] and 'CU' in p['brand']:
        test_urls.append((p['name'], p['brand'], p['image']))
        break
for p in d['products']:
    if '멘토스' in p['name'] and 'CU' in p['brand']:
        test_urls.append((p['name'], p['brand'], p['image']))
        break
for p in d['products']:
    if '육개장' in p['name'] and 'GS25' in p['brand']:
        test_urls.append((p['name'], p['brand'], p['image']))
        break

print('Testing image URL accessibility:')
print('=' * 80)
for name, brand, url in test_urls:
    try:
        req = urllib.request.Request(url, method='HEAD', headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://pyony.com/'
        })
        res = urllib.request.urlopen(req, timeout=5)
        content_type = res.info().get('Content-Type', 'unknown')
        status = res.status
        print(f'  ✅ {status} [{content_type}] [{brand}] {name}')
        print(f'     {url}')
    except urllib.error.HTTPError as e:
        print(f'  ❌ HTTP {e.code} [{brand}] {name}')
        print(f'     {url}')
    except Exception as e:
        print(f'  ❌ Error [{brand}] {name}: {e}')
        print(f'     {url}')
