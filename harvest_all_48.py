import urllib.request
import urllib.parse
import json
import base64
import subprocess
import re
import time

API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

# List of 48 products that need dedicated real packaging images
PRODUCTS_TO_FIX = [
    "코카콜라 500ml",
    "코카콜라 제로 500ml",
    "칠성사이다 500ml",
    "칠성사이다 제로 500ml",
    "스프라이트 500ml",
    "환타 오렌지 600ml",
    "펩시콜라 제로 라임 500ml",
    "아이시스 8.0 500ml",
    "광동 옥수수수수차 500ml",
    "HK 헛개수 500ml",
    "현대 미에로화이바 350ml",
    "몬스터에너지 355ml",
    "핫식스 250ml",
    "레드불 250ml",
    "조지아 크래프트 아메리카노 470ml",
    "칸타타 프리미엄 라떼 275ml",
    "TOP 마스터라떼 275ml",
    "매일 바리스타룰스 모카 250ml",
    "매일 바리스타룰스 디카페인 250ml",
    "빙그레 아카페라 바닐라라떼 240ml",
    "스타벅스 파이크플레이스 블랙 275ml",
    "농심 육개장 사발면 86g",
    "오뚜기 참깨라면 컵",
    "혜자로운집밥 제육볶음도시락",
    "백종원 매콤제육 정식도시락",
    "서울우유 딸기우유 300ml",
    "서울우유 초코우유 300ml",
    "덴마크 드링킹요구르트 딸기 310ml",
    "풀무원 액티비아업 딸기 210ml",
    "연세우유 생크림빵 130g",
    "하겐다즈 파인트 바닐라 473ml",
    "하겐다즈 스틱바 딸기",
    "나뚜루 파인트 녹차 474ml",
    "롯데 월드콘 바닐라 160ml",
    "빙그레 메로나 70ml",
    "해태 허니버터칩 60g",
    "농심 멘토스 푸르티 37g",
    "오리온 초코파이 12입 팩",
    "2080 초극세모 미세모 칫솔",
    "페리오 토탈7 알파 치약",
    "크리넥스 수프림소프트 30롤",
    "좋은느낌 유기농 라이너 18P",
    "가그린 제로 구강청결제 750ml",
    "여명808 숙취해소음료 140ml",
    "2080 토탈 전문 치약 120g",
    "리스테린 쿨민트 구강청결제 750ml",
    "컨디션 스틱 헛개 18g",
    "농심 신라면 컵 65g"
]

def harvest_real_product_image(product_name):
    query = f"{product_name} 누끼 상품 이미지"
    encoded = urllib.parse.quote(query)
    url = f"https://m.search.naver.com/search.naver?where=m_image&query={encoded}"
    cmd = [
        "curl.exe", "-s", "-L",
        "-H", "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        html = res.stdout
        imgs = re.findall(r'https://search\.pstatic\.net/[^"\'\s<>\\]+', html)
        
        shopping_imgs = []
        other_imgs = []
        for img in imgs:
            decoded = urllib.parse.unquote(img)
            if any(cdn in decoded for cdn in ['lotteon.com', 'ssgcdn.com', 'coupangcdn.com', '011st.com', 'shop1.phinf.naver.net', 'shop-phinf.pstatic.net', 'wemep.co.kr', 'gmarket.co.kr', 'homeplus.co.kr', 'enuri.com']):
                shopping_imgs.append(decoded)
            elif not any(x in decoded for x in ['blogpfthumb', 'type=f', 'logo', 'icon']):
                other_imgs.append(decoded)
                
        candidates = shopping_imgs + other_imgs
        for candidate in candidates[:5]:
            try:
                req = urllib.request.Request(candidate, headers={"User-Agent": "Mozilla/5.0"})
                img_bytes = urllib.request.urlopen(req, timeout=8).read()
                if len(img_bytes) > 2000:
                    return img_bytes
            except Exception:
                continue
    except Exception as e:
        print(f"Scrape error for {product_name}: {e}")
    return None

def upload_b64_to_imgbb(img_bytes, filename):
    try:
        b64_data = base64.b64encode(img_bytes).decode("utf-8")
        post_data = urllib.parse.urlencode({
            "key": API_KEY,
            "image": b64_data,
            "name": filename
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.imgbb.com/1/upload",
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        res = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
        res_json = json.loads(res)
        if res_json.get("success"):
            return res_json["data"]["url"]
    except Exception as e:
        print(f"ImgBB upload error for {filename}: {e}")
    return None

def run_harvest_all():
    results = {}
    print(f"Starting harvest and upload for {len(PRODUCTS_TO_FIX)} products...")
    
    for idx, p in enumerate(PRODUCTS_TO_FIX, 1):
        print(f"[{idx}/{len(PRODUCTS_TO_FIX)}] Harvesting: {p}")
        img_bytes = harvest_real_product_image(p)
        if img_bytes:
            imgbb_url = upload_b64_to_imgbb(img_bytes, p)
            if imgbb_url:
                results[p] = imgbb_url
                print(f"  SUCCESS => {imgbb_url}")
            else:
                print("  FAILED ImgBB Upload")
        else:
            print("  FAILED Harvest Image Bytes")
        time.sleep(0.2)
        
    with open("harvested_48_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"\nCompleted! Harvested {len(results)} / {len(PRODUCTS_TO_FIX)} products into harvested_48_results.json")

if __name__ == "__main__":
    run_harvest_all()
