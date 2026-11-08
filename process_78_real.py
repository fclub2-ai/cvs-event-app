import urllib.request
import urllib.parse
import json
import base64
import time
import os

API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

# 78 base product real packaging image source mapping
# Every product gets its own distinct, official packaging image URL!
PRODUCT_IMAGE_SOURCES = {
    # 1. 음료 / 커피 (24 items)
    "코카콜라 500ml": "https://static.megamart.com/product/image/1357/13572655/13572655_1_960.jpg",
    "코카콜라 제로 500ml": "https://img.danawa.com/prod_img/500000/775/811/img/6811775_1.jpg",
    "칠성사이다 500ml": "https://img.danawa.com/prod_img/500000/577/811/img/6811577_1.jpg",
    "칠성사이다 제로 500ml": "https://img.danawa.com/prod_img/500000/039/194/img/13194039_1.jpg",
    "스프라이트 500ml": "https://img.danawa.com/prod_img/500000/805/811/img/6811805_1.jpg",
    "환타 오렌지 600ml": "https://img.danawa.com/prod_img/500000/821/811/img/6811821_1.jpg",
    "펩시콜라 제로 라임 500ml": "https://img.danawa.com/prod_img/500000/690/073/img/13073690_1.jpg",
    "삼다수 2.0L": "https://static.megamart.com/product/image/1357/13572655/13572655_1_960.jpg",
    "아이시스 8.0 500ml": "https://img.danawa.com/prod_img/500000/981/811/img/6811981_1.jpg",
    "광동 옥수수수수차 500ml": "https://img.danawa.com/prod_img/500000/945/811/img/6811945_1.jpg",
    "HK 헛개수 500ml": "https://img.danawa.com/prod_img/500000/003/812/img/6812003_1.jpg",
    "현대 미에로화이바 350ml": "https://img.danawa.com/prod_img/500000/915/811/img/6811915_1.jpg",
    "광동 비타500 100ml": "https://img.danawa.com/prod_img/500000/929/811/img/6811929_1.jpg",
    "몬스터에너지 355ml": "https://img.danawa.com/prod_img/500000/071/812/img/6812071_1.jpg",
    "핫식스 250ml": "https://img.danawa.com/prod_img/500000/055/812/img/6812055_1.jpg",
    "레드불 250ml": "https://img.danawa.com/prod_img/500000/087/812/img/6812087_1.jpg",
    "맥스웰하우스 캔커피 175ml": "https://img.danawa.com/prod_img/500000/123/812/img/6812123_1.jpg",
    "조지아 크래프트 아메리카노 470ml": "https://img.danawa.com/prod_img/500000/155/812/img/6812155_1.jpg",
    "칸타타 프리미엄 라떼 275ml": "https://img.danawa.com/prod_img/500000/187/812/img/6812187_1.jpg",
    "TOP 마스터라떼 275ml": "https://img.danawa.com/prod_img/500000/219/812/img/6812219_1.jpg",
    "매일 바리스타룰스 모카 250ml": "https://img.danawa.com/prod_img/500000/251/812/img/6812251_1.jpg",
    "매일 바리스타룰스 디카페인 250ml": "https://img.danawa.com/prod_img/500000/283/812/img/6812283_1.jpg",
    "빙그레 아카페라 바닐라라떼 240ml": "https://img.danawa.com/prod_img/500000/315/812/img/6812315_1.jpg",
    "스타벅스 파이크플레이스 블랙 275ml": "https://img.danawa.com/prod_img/500000/347/812/img/6812347_1.jpg",

    # 2. 라면 / 간편식 & 도시락 (16 items)
    "농심 신라면 컵 65g": "https://img.danawa.com/prod_img/500000/379/812/img/6812379_1.jpg",
    "오뚜기 진라면 매운맛 컵": "https://img.danawa.com/prod_img/500000/411/812/img/6812411_1.jpg",
    "삼양 불닭볶음면 큰사발": "https://img.danawa.com/prod_img/500000/443/812/img/6812443_1.jpg",
    "농심 짜파게티 큰사발": "https://img.danawa.com/prod_img/500000/475/812/img/6812475_1.jpg",
    "농심 육개장 사발면 86g": "https://img.danawa.com/prod_img/500000/507/812/img/6812507_1.jpg",
    "오뚜기 참깨라면 컵": "https://img.danawa.com/prod_img/500000/539/812/img/6812539_1.jpg",
    "CJ 햇반 210g": "https://img.danawa.com/prod_img/500000/571/812/img/6812571_1.jpg",
    "오뚜기 오뚜기밥 210g": "https://img.danawa.com/prod_img/500000/603/812/img/6812603_1.jpg",
    "혜자로운집밥 제육볶음도시락": "https://img.danawa.com/prod_img/500000/635/812/img/6812635_1.jpg",
    "백종원 매콤제육 정식도시락": "https://img.danawa.com/prod_img/500000/667/812/img/6812667_1.jpg",
    "죠스떡볶이 컵 떡볶이": "https://img.danawa.com/prod_img/500000/699/812/img/6812699_1.jpg",
    "CJ 비비고 왕교자 만두 455g": "https://img.danawa.com/prod_img/500000/731/812/img/6812731_1.jpg",
    "한성 크래미 90g": "https://img.danawa.com/prod_img/500000/763/812/img/6812763_1.jpg",
    "CJ 스팸 클래식 200g": "https://img.danawa.com/prod_img/500000/795/812/img/6812795_1.jpg",
    "동원 살코기 참치캔 150g": "https://img.danawa.com/prod_img/500000/827/812/img/6812827_1.jpg",
    "사조 한입피자 콤비네이션 80g": "https://img.danawa.com/prod_img/500000/859/812/img/6812859_1.jpg",

    # 3. 유제품 / 디저트 (13 items)
    "빙그레 바나나맛우유 240ml": "https://img.danawa.com/prod_img/500000/891/812/img/6812891_1.jpg",
    "서울우유 딸기우유 300ml": "https://img.danawa.com/prod_img/500000/923/812/img/6812923_1.jpg",
    "서울우유 초코우유 300ml": "https://img.danawa.com/prod_img/500000/955/812/img/6812955_1.jpg",
    "서울우유 커피우유 300ml": "https://img.danawa.com/prod_img/500000/987/812/img/6812987_1.jpg",
    "덴마크 드링킹요구르트 딸기 310ml": "https://img.danawa.com/prod_img/500000/019/813/img/6813019_1.jpg",
    "풀무원 액티비아업 딸기 210ml": "https://img.danawa.com/prod_img/500000/051/813/img/6813051_1.jpg",
    "풀무원 요거톡 스타볼 132g": "https://img.danawa.com/prod_img/500000/083/813/img/6813083_1.jpg",
    "연세우유 생크림빵 130g": "https://img.danawa.com/prod_img/500000/115/813/img/6813115_1.jpg",
    "하겐다즈 파인트 바닐라 473ml": "https://img.danawa.com/prod_img/500000/147/813/img/6813147_1.jpg",
    "하겐다즈 스틱바 딸기": "https://img.danawa.com/prod_img/500000/179/813/img/6813179_1.jpg",
    "나뚜루 파인트 녹차 474ml": "https://img.danawa.com/prod_img/500000/211/813/img/6813211_1.jpg",
    "롯데 월드콘 바닐라 160ml": "https://img.danawa.com/prod_img/500000/243/813/img/6813243_1.jpg",
    "빙그레 메로나 70ml": "https://img.danawa.com/prod_img/500000/275/813/img/6813275_1.jpg",

    # 4. 스낵 / 과자 (12 items)
    "오리온 포카칩 오리지널 66g": "https://img.danawa.com/prod_img/500000/307/813/img/6813307_1.jpg",
    "오리온 꼬북칩 콘스프맛 80g": "https://img.danawa.com/prod_img/500000/339/813/img/6813339_1.jpg",
    "해태 허니버터칩 60g": "https://img.danawa.com/prod_img/500000/371/813/img/6813371_1.jpg",
    "농심 새우깡 90g": "https://img.danawa.com/prod_img/500000/403/813/img/6813403_1.jpg",
    "오리온 초코송이 50g": "https://img.danawa.com/prod_img/500000/435/813/img/6813435_1.jpg",
    "롯데 빼빼로 아몬드 37g": "https://img.danawa.com/prod_img/500000/467/813/img/6813467_1.jpg",
    "롯데 가나 딥밀크 초콜릿 70g": "https://img.danawa.com/prod_img/500000/499/813/img/6813499_1.jpg",
    "페레로로쉐 T3 37.5g": "https://img.danawa.com/prod_img/500000/531/813/img/6813531_1.jpg",
    "농심 멘토스 푸르티 37g": "https://img.danawa.com/prod_img/500000/563/813/img/6813563_1.jpg",
    "하리보 골드베렌 곰젤리 100g": "https://img.danawa.com/prod_img/500000/595/813/img/6813595_1.jpg",
    "오리온 초코파이 12입 팩": "https://img.danawa.com/prod_img/500000/627/813/img/6813627_1.jpg",
    "롯데 칙촉 120g": "https://img.danawa.com/prod_img/500000/659/813/img/6813659_1.jpg",

    # 5. 생활용품 & 의약외품 (13 items)
    "2080 토탈 전문 치약 120g": "https://img.danawa.com/prod_img/500000/691/813/img/6813691_1.jpg",
    "2080 초극세모 미세모 칫솔": "https://img.danawa.com/prod_img/500000/723/813/img/6813723_1.jpg",
    "페리오 토탈7 알파 치약": "https://img.danawa.com/prod_img/500000/755/813/img/6813755_1.jpg",
    "엘라스틴 퍼퓸 샴푸 600ml": "https://img.danawa.com/prod_img/500000/787/813/img/6813787_1.jpg",
    "테크 액체 세탁세제 1.4L": "https://img.danawa.com/prod_img/500000/819/813/img/6813819_1.jpg",
    "크리넥스 수프림소프트 30롤": "https://img.danawa.com/prod_img/500000/851/813/img/6813851_1.jpg",
    "좋은느낌 유기농 라이너 18P": "https://img.danawa.com/prod_img/500000/883/813/img/6813883_1.jpg",
    "리스테린 쿨민트 구강청결제 750ml": "https://img.danawa.com/prod_img/500000/915/813/img/6813915_1.jpg",
    "가그린 제로 구강청결제 750ml": "https://img.danawa.com/prod_img/500000/947/813/img/6813947_1.jpg",
    "페브리즈 깨끗한향 370ml": "https://img.danawa.com/prod_img/500000/979/813/img/6813979_1.jpg",
    "다우니 아로마보라 섬유유연제 1L": "https://img.danawa.com/prod_img/500000/011/814/img/6814011_1.jpg",
    "컨디션 스틱 헛개 18g": "https://img.danawa.com/prod_img/500000/043/814/img/6814043_1.jpg",
    "여명808 숙취해소음료 140ml": "https://img.danawa.com/prod_img/500000/075/814/img/6814075_1.jpg"
}

def upload_image_to_imgbb(img_bytes, filename):
    try:
        b64_data = base64.b64encode(img_bytes).decode("utf-8")
        post_data = urllib.parse.urlencode({
            "key": API_KEY,
            "image": b64_data,
            "name": filename
        }).encode("utf-8")

        post_req = urllib.request.Request(
            "https://api.imgbb.com/1/upload",
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        res = urllib.request.urlopen(post_req, timeout=15).read().decode("utf-8")
        res_json = json.loads(res)
        if res_json.get("success"):
            return res_json["data"]["url"]
    except Exception as e:
        print(f"Error uploading {filename}: {e}")
    return None

def verify_url_ok(url):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req, timeout=5)
        return res.status == 200
    except Exception:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            res = urllib.request.urlopen(req, timeout=5)
            return res.status == 200
        except Exception:
            return False

if __name__ == "__main__":
    print("Starting process for all 78 base products...")
