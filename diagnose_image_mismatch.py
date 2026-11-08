"""
이미지 매칭 진단 스크립트
- pyony.com에서 실시간으로 스크랩한 (상품명, 이미지URL) 쌍과
  cvs_data.json에 저장된 (상품명, 이미지URL) 쌍을 비교해서
  불일치가 어디서 발생하는지 정확히 찾아냄
"""

import sys, gzip, urllib.request, json, re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Encoding": "gzip"
}

def scrape_one_page(brand_slug, page):
    """pyony.com 한 페이지에서 (상품명, 이미지URL) 목록을 가져옴"""
    url = f"https://pyony.com/brands/{brand_slug}/?page={page}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, timeout=15)
        raw = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            html = gzip.decompress(raw).decode('utf-8', errors='ignore')
        else:
            html = raw.decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".col-md-6")
        results = []
        for c in cards:
            strong = c.select_one(".card-body strong")
            img = c.select_one("img.prod_img")
            if strong and img:
                name = strong.get_text(strip=True)
                src = img.get("src", "")
                if src.startswith("//"):
                    src = "https:" + src
                results.append((name, src))
        return results
    except Exception as e:
        print(f"  [ERROR] {url}: {e}")
        return []

# Step 1: CU 1페이지에서 실제 상품-이미지 매핑 확인
print("=" * 80)
print("STEP 1: pyony.com/brands/cu/ 1페이지 실시간 스크랩 결과")
print("=" * 80)
cu_page1 = scrape_one_page("cu", 1)
for name, img in cu_page1[:15]:
    print(f"  [{name}] => {img}")

# Step 2: cvs_data.json에서 같은 상품 찾아서 비교
print("\n" + "=" * 80)
print("STEP 2: cvs_data.json에 저장된 같은 상품들의 이미지 비교")
print("=" * 80)
with open("backend/cvs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

db_products = data.get("products", [])

# CU 페이지 첫 15개 상품에 대해 cvs_data.json에서 찾기
mismatch_count = 0
for pyony_name, pyony_img in cu_page1[:15]:
    # cvs_data에서 같은 이름의 상품 찾기
    found = False
    for db_p in db_products:
        if pyony_name in db_p["name"] or db_p["name"] in pyony_name:
            status = "✅ MATCH" if db_p["image"] == pyony_img else "❌ MISMATCH"
            if db_p["image"] != pyony_img:
                mismatch_count += 1
            print(f"  {status}")
            print(f"    상품명: {pyony_name}")
            print(f"    Pyony 원본: {pyony_img}")
            print(f"    DB 저장값:  {db_p['image']}")
            print()
            found = True
            break
    if not found:
        print(f"  ⚠️ NOT FOUND in DB: {pyony_name}")
        print()

print(f"\n불일치 건수: {mismatch_count} / {min(15, len(cu_page1))}")

# Step 3: GS25 1페이지도 확인
print("\n" + "=" * 80)
print("STEP 3: pyony.com/brands/gs25/ 1페이지 실시간 스크랩 vs DB")
print("=" * 80)
gs_page1 = scrape_one_page("gs25", 1)
mismatch_gs = 0
for pyony_name, pyony_img in gs_page1[:10]:
    found = False
    for db_p in db_products:
        if pyony_name in db_p["name"] or db_p["name"] in pyony_name:
            status = "✅ MATCH" if db_p["image"] == pyony_img else "❌ MISMATCH"
            if db_p["image"] != pyony_img:
                mismatch_gs += 1
            print(f"  {status}")
            print(f"    상품명: {pyony_name}")
            print(f"    Pyony: {pyony_img}")
            print(f"    DB:    {db_p['image']}")
            print()
            found = True
            break
    if not found:
        print(f"  ⚠️ NOT FOUND in DB: {pyony_name}")
        print()

print(f"\n불일치 건수: {mismatch_gs} / {min(10, len(gs_page1))}")

# Step 4: 스크린샷에서 보인 문제 상품들 직접 확인
print("\n" + "=" * 80)
print("STEP 4: 스크린샷 문제 상품 직접 조사")
print("=" * 80)
problem_names = [
    "새콤달콤", "비타500", "육개장", "멘토스", "맥스웰하우스", "코카콜라"
]
for keyword in problem_names:
    matches = [p for p in db_products if keyword in p["name"]]
    print(f"\n  ===== '{keyword}' 관련 상품 ({len(matches)}건) =====")
    for m in matches[:4]:
        print(f"    [{m['brand']}] {m['name']}")
        print(f"      image: {m['image']}")
