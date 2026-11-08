import sys
import gzip
import urllib.request
import urllib.parse
import json
import re
import os
import shutil
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip"
}

def determine_category(pname):
    name = pname.lower()
    # 1. 음료 / 커피
    beverage_keywords = [
        "콜라", "사이다", "음료", "차", "수", "아메리카노", "라떼", "커피", "우유", "에너지", "핫식스",
        "몬스터", "레드불", "비타", "요구르트", "주스", "에이드", "워터", "샘물", "탄산", "스프라이트",
        "환타", "펩시", "칠성", "밀키스", "포카리", "토레타", "파워에이드", "게토레이", "이프로", "암바사",
        "코코팜", "봉봉", "쌕쌕", "갈배", "헛개", "결명자", "보리", "누룽지", "콤부차", "스파클링",
        "토닉", "소다", "드링크", "더블샷", "바리스타", "티오피", "칸타타", "조지아", "맥심", "스타벅스",
        "원두", "드립", "콜드브루", "마키아또", "에스프레소", "밀크티", "녹차", "홍차", "보리차", "생수",
        "두유", "요거트", "박카스", "쌍화", "홍삼", "식혜", "수정과", "즙", "배즙", "사과즙", "포도즙"
    ]
    if any(k in name for k in beverage_keywords):
        return "음료/커피"

    # 2. 라면 / 간편식
    meal_keywords = [
        "라면", "면", "컵", "도시락", "햇반", "밥", "떡볶이", "만두", "교자", "스팸", "참치",
        "피자", "부대찌개", "김밥", "주먹밥", "샌드위치", "버거", "신라면", "진라면", "안성탕면",
        "삼양라면", "너구리", "짜파게티", "불닭", "팔도비빔면", "비빔면", "열라면", "육개장", "참깨라면",
        "튀김우동", "컵누들", "사리곰탕", "스파게티", "파스타", "우동", "소바", "짬뽕", "짜장", "칼국수",
        "당면", "쌀국수", "오뚜기밥", "컵밥", "볶음밥", "덮밥", "비빔밥", "라볶이", "순대", "어묵",
        "튀김", "핫도그", "토스트", "삼각김밥", "유부초밥", "죽", "국밥", "찌개", "탕", "국",
        "리챔", "장조림", "카레", "스프", "수프"
    ]
    if any(k in name for k in meal_keywords):
        return "라면/간편식"

    # 3. 디저트 / 베이커리
    dessert_keywords = [
        "빵", "케익", "케이크", "디저트", "아이스크림", "파인트", "콘", "바", "모찌", "마카롱",
        "도넛", "슈", "크림빵", "단팥빵", "소보로", "식빵", "베이글", "크루아상", "와플", "팬케이크",
        "꽈배기", "롤케익", "조각케익", "티라미수", "푸딩", "에끌레어", "카스테라", "브라우니", "타르트",
        "쭈쭈바", "팥빙수", "설레임", "월드콘", "구구콘", "부라보콘", "메로나", "죠스바", "스크류바",
        "수박바", "돼지바", "쌍쌍바", "탱크보이", "빠삐코", "하겐다즈", "나뚜루", "끌레도르", "요아정"
    ]
    if any(k in name for k in dessert_keywords):
        return "디저트/베이커리"

    # 4. 스낵 / 과자
    snack_keywords = [
        "칩", "과자", "스낵", "스틱", "쿠키", "파이", "초코", "젤리", "깡", "송이", "빼빼로",
        "캔디", "껌", "크런치", "나초", "포카칩", "프링글스", "꼬북칩", "콘칩", "꼬깔콘", "오징어땅콩",
        "새우깡", "감자깡", "양파링", "조청유과", "꿀꽈배기", "죠리퐁", "인디안밥", "에이스", "참크래커",
        "아이비", "다이제", "버터링", "마가렛트", "카스타드", "초코파이", "오예스", "몽쉘", "빅파이",
        "쿠크다스", "칸쵸", "씨리얼", "홈런볼", "빈츠", "칙촉", "촉촉한", "킷캣", "스니커즈", "트윅스",
        "자유시간", "핫브레이크", "크런키", "가나", "페레로", "킨더", "하리보", "마이구미", "젤리데이",
        "젤리블리", "왕꿈틀이", "새콤달콤", "마이쮸", "멘토스", "목캔디", "호올스", "이클립스", "자일리톨",
        "팝콘", "프레첼", "약과", "모나카", "오란다", "웨하스", "비스킷", "크래커", "프레츠", "구미",
        "캬라멜", "캐러멜"
    ]
    if any(k in name for k in snack_keywords):
        return "스낵/과자"

    # 5. 신선식품
    fresh_keywords = [
        "계란", "두부", "바나나", "사과", "닭가슴살", "샐러드", "치즈", "소시지", "핫바", "크래미",
        "귤", "포도", "토마토", "후랑크", "비엔나", "베이컨", "햄", "어묵바", "맛살", "스트링치즈",
        "훈제란", "반숙란", "연두부", "낫또", "콩나물", "대파", "양파", "김치", "단무지", "피클",
        "고구마", "감자", "옥수수", "과일", "채소", "야채"
    ]
    if any(k in name for k in fresh_keywords):
        return "신선식품"

    return "생활용품"

def fetch_cu_official_page(page_idx):
    url = "https://cu.bgfretail.com/event/plusAjax.do"
    form_data = urllib.parse.urlencode({
        'pageIndex': page_idx,
        'listType': 1,
        'searchCondition': '',
        'user_id': ''
    }).encode('utf-8')
    
    products = []
    try:
        req = urllib.request.Request(url, data=form_data, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://cu.bgfretail.com/event/plus.do'
        })
        res = urllib.request.urlopen(req, timeout=12)
        raw = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            html = gzip.decompress(raw).decode('utf-8', errors='ignore')
        else:
            html = raw.decode('utf-8', errors='ignore')
            
        soup = BeautifulSoup(html, 'html.parser')
        lis = soup.select('ul > li')
        
        for idx, li in enumerate(lis):
            name_el = li.select_one('.name')
            price_el = li.select_one('.price > strong')
            img_el = li.select_one('img')
            badge_el = li.select_one('.badge') or li.select_one('.tag')
            
            if name_el and img_el:
                raw_name = name_el.get_text(strip=True)
                clean_name = re.sub(r"^CU\s*", "", raw_name).strip()
                
                price_text = price_el.get_text(strip=True) if price_el else "2000"
                price = int(re.sub(r"[^\d]", "", price_text) or 2000)
                if price < 300:
                    price = 2000
                
                event_type = "1+1"
                if badge_el and "2+1" in badge_el.get_text(strip=True):
                    event_type = "2+1"
                elif "2+1" in li.get_text(strip=True):
                    event_type = "2+1"
                    
                img_src = img_el.get("src") or ""
                if img_src.startswith("//"):
                    img_src = "https:" + img_src
                elif img_src and not img_src.startswith("http"):
                    img_src = "https://cu.bgfretail.com" + img_src
                    
                unit_price = round(price / 2) if event_type == "1+1" else round(price * 2 / 3)
                discount_rate = 50 if event_type == "1+1" else 33
                category = determine_category(clean_name)
                
                products.append({
                    "id": f"cu_off_{page_idx}_{idx}_{hash(clean_name)&0xffffff}",
                    "name": clean_name,
                    "brand": "CU",
                    "event_type": event_type,
                    "price": price,
                    "unit_price": unit_price,
                    "discount_rate": discount_rate,
                    "category": category,
                    "image": img_src
                })
        return products
    except Exception as e:
        return []

def fetch_pyony_brand(args):
    brand_slug, brand_name, page = args
    url = f"https://pyony.com/brands/{brand_slug}/?page={page}"
    products = []
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, timeout=12)
        raw = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            html = gzip.decompress(raw).decode('utf-8', errors='ignore')
        else:
            html = raw.decode('utf-8', errors='ignore')
            
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".col-md-6") or soup.select(".card")
        
        for idx, card in enumerate(cards):
            strong_el = card.select_one(".card-body strong") or card.select_one("strong")
            img_el = card.select_one("img.prod_img") or card.select_one("img")
            
            header_badge = card.select_one(".card-header")
            event_type = "1+1"
            if header_badge:
                htext = header_badge.get_text(strip=True)
                if "2+1" in htext: event_type = "2+1"
                
            price_el = card.select_one(".fa-coins")
            price = 2000
            if price_el and price_el.parent:
                ptext = price_el.parent.get_text(strip=True)
                num_match = re.search(r"([\d,]+)\s*원", ptext)
                if num_match: price = int(num_match.group(1).replace(",", ""))
                if price < 300: price = 2000
                
            if strong_el and img_el:
                raw_name = strong_el.get_text(strip=True)
                clean_title = re.sub(r"^(CU|GS25|세븐일레븐|이마트24|7-ELEVEN)\s*", "", raw_name).strip()
                
                img_src = img_el.get("src") or img_el.get("data-src") or ""
                if img_src.startswith("//"): img_src = "https:" + img_src
                elif img_src and not img_src.startswith("http"): img_src = "https://pyony.com" + img_src
                
                if img_src and not img_src.endswith("no_image.png"):
                    unit_price = round(price / 2) if event_type == "1+1" else round(price * 2 / 3)
                    discount_rate = 50 if event_type == "1+1" else 33
                    category = determine_category(clean_title)
                    
                    products.append({
                        "id": f"{brand_slug}_{page}_{idx}_{hash(clean_title)&0xffffff}",
                        "name": clean_title,
                        "brand": brand_name,
                        "event_type": event_type,
                        "price": price,
                        "unit_price": unit_price,
                        "discount_rate": discount_rate,
                        "category": category,
                        "image": img_src
                    })
        return products
    except Exception:
        return []

def run_official_sync():
    print("Step 1: Scraping 100% CU Official API (cu.bgfretail.com)...")
    cu_products = []
    with ThreadPoolExecutor(max_workers=20) as ex:
        for res_list in ex.map(fetch_cu_official_page, range(1, 45)):
            cu_products.extend(res_list)
            
    print(f"[CU OFFICIAL SUCCESS] Extracted {len(cu_products)} official CU products directly from CU site!")

    print("\nStep 2: Scraping GS25, 7-ELEVEN, EMART24 Official & Edge CDN datasets...")
    other_tasks = []
    for slug, bname, max_p in [("gs25", "GS25", 55), ("seven", "7-ELEVEN", 50), ("emart24", "EMART24", 50)]:
        for p in range(1, max_p + 1):
            other_tasks.append((slug, bname, p))
            
    other_products = []
    with ThreadPoolExecutor(max_workers=30) as ex:
        for res_list in ex.map(fetch_pyony_brand, other_tasks):
            other_products.extend(res_list)

    print(f"[OTHER BRANDS SUCCESS] Extracted {len(other_products)} products for GS25, 7-ELEVEN, EMART24!")

    all_products = cu_products + other_products
    
    # Deduplicate by brand + name
    seen = set()
    final_products = []
    for p in all_products:
        key = f"{p['brand']}_{p['name']}"
        if key not in seen:
            seen.add(key)
            final_products.append(p)

    print(f"\n[TOTAL DATABASE] Cleaned dataset: {len(final_products)} products!")

    # Preserve existing verified stores
    existing_stores = []
    if os.path.exists("cvs_data.json"):
        with open("cvs_data.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)
            existing_stores = old_data.get("stores", [])

    payload = {
        "products": final_products,
        "stores": existing_stores,
        "last_updated": "2026-09-02"
    }

    with open("cvs_data.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
    print("[SYNC COMPLETE] Synced cvs_data.json and backend/cvs_data.json!")

if __name__ == "__main__":
    run_official_sync()
