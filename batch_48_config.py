import urllib.request
import urllib.parse
import json
import base64
import time
import os

API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

# Prompts for 48 products to generate hyper-realistic official product packaging studio photos
ITEMS_TO_GENERATE = {
    "코카콜라 500ml": "Official product packaging studio photograph of Coca-Cola 500ml PET bottle on plain white background. Iconic red label with white script, clear plastic bottle filled with dark cola, red cap, 4k commercial product photo",
    "코카콜라 제로 500ml": "Official product packaging studio photograph of Coca-Cola Zero Sugar 500ml PET bottle on plain white background. Black label with red Coca-Cola logo and 'Zero Sugar' text, black cap, commercial product shot",
    "칠성사이다 500ml": "Official product packaging studio photograph of Chilsung Cider 500ml bottle on white background. Green plastic PET bottle with iconic white star and green Chilsung logo label, green cap",
    "칠성사이다 제로 500ml": "Official product packaging studio photograph of Chilsung Cider Zero 500ml bottle on white background. Clear/green bottle with 'Zero Sugar' label design, studio product photo",
    "스프라이트 500ml": "Official product packaging studio photograph of Sprite 500ml PET bottle on clean white background. Bright green bottle with yellow lemon lime Sprite logo label, green cap",
    "환타 오렌지 600ml": "Official product packaging studio photograph of Fanta Orange 600ml bottle on white background. Bright orange soda bottle with blue and orange Fanta logo label, orange cap",
    "펩시콜라 제로 라임 500ml": "Official product packaging studio photograph of Pepsi Zero Sugar Lime 500ml PET bottle on white background. Black bottle label with lime green accent ring and Pepsi globe logo",
    "아이시스 8.0 500ml": "Official product packaging studio photograph of Lotte ICIS 8.0 500ml mineral water bottle on white background. Pink and blue label with clear spring water",
    "광동 옥수수수수차 500ml": "Official product packaging studio photograph of Kwangdong Corn Silk Tea 500ml PET bottle on white background. Warm amber tea bottle with Korean corn tea label",
    "HK 헛개수 500ml": "Official product packaging studio photograph of HK inno.N Heutgae-soo 500ml oriental raisin tea bottle on white background. Dark brown tea bottle with brown label",
    "현대 미에로화이바 350ml": "Official product packaging studio photograph of Miero Fiber 350ml glass bottle on white background. Glass bottle with bright orange fiber drink label and orange cap",
    "몬스터에너지 355ml": "Official product packaging studio photograph of Monster Energy 355ml aluminum can on white background. Matte black can with vibrant neon green claw M logo",
    "핫식스 250ml": "Official product packaging studio photograph of Lotte Hot6 Energy Drink 250ml aluminum can on white background. Silver and red energy can with phoenix logo",
    "레드불 250ml": "Official product packaging studio photograph of Red Bull Energy Drink 250ml silver and blue can on white background with yellow and red bulls logo",
    "조지아 크래프트 아메리카노 470ml": "Official product packaging studio photograph of Georgia Craft Americano 470ml coffee bottle on white background. Tall clear bottle with dark black coffee and brown coffee label",
    "칸타타 프리미엄 라떼 275ml": "Official product packaging studio photograph of Lotte Cantata Premium Latte 275ml NB aluminum bottle can on white background. Metallic coffee bottle with golden brown latte design",
    "TOP 마스터라떼 275ml": "Official product packaging studio photograph of Maxim T.O.P Master Latte 275ml aluminum bottle can on white background. Black and gold premium espresso coffee bottle can",
    "매일 바리스타룰스 모카 250ml": "Official product packaging studio photograph of Barista Rules Mocha 250ml plastic cup with straw on white background. Dark brown coffee cup package",
    "매일 바리스타룰스 디카페인 250ml": "Official product packaging studio photograph of Barista Rules Decafe 250ml plastic coffee cup with straw on white background. Blue and brown coffee cup package",
    "빙그레 아카페라 바닐라라떼 240ml": "Official product packaging studio photograph of Binggrae Acapella Vanilla Latte 240ml bottle on white background. Soft beige vanilla coffee bottle package",
    "스타벅스 파이크플레이스 블랙 275ml": "Official product packaging studio photograph of Starbucks Pike Place Roast Black Coffee 275ml can on white background. Premium dark green Starbucks coffee can with siren logo",
    "농심 육개장 사발면 86g": "Official product packaging studio photograph of Nongshim Yukgaejang Bowl Noodle 86g bowl instant ramen on white background. Iconic square-round paper bowl with orange red lid design",
    "오뚜기 참깨라면 컵": "Official product packaging studio photograph of Ottogi Sesame Ramyun Cup instant noodle on white background. Yellow and red cup noodle packaging with egg and sesame icon",
    "혜자로운집밥 제육볶음도시락": "Official product packaging studio photograph of GS25 Hyeja Spicy Pork Jeyuk Bento Box meal packaging on white background. Korean convenience store bento box package",
    "백종원 매콤제육 정식도시락": "Official product packaging studio photograph of CU Baek Jong-won Spicy Pork Lunch Box bento packaging on white background. Convenience store bento box",
    "서울우유 딸기우유 300ml": "Official product packaging studio photograph of Seoul Milk Strawberry 300ml carton on white background. Pink and white milk carton with strawberry image",
    "서울우유 초코우유 300ml": "Official product packaging studio photograph of Seoul Milk Chocolate 300ml carton on white background. Dark brown and white chocolate milk carton",
    "덴마크 드링킹요구르트 딸기 310ml": "Official product packaging studio photograph of Denmark Drinking Yogurt Strawberry 310ml carton on white background. Pink yogurt drink carton with strawberry graphic",
    "풀무원 액티비아업 딸기 210ml": "Official product packaging studio photograph of Pulmuone Activia Up Strawberry 210ml bottle on white background. Green and pink probiotic yogurt bottle",
    "연세우유 생크림빵 130g": "Official product packaging studio photograph of Yonsei University Milk Cream Bread 130g plastic package on white background. Famous cream-filled pastry bag",
    "하겐다즈 파인트 바닐라 473ml": "Official product packaging studio photograph of Haagen-Dazs Vanilla Ice Cream Pint 473ml tub on white background. Burgundy and gold premium ice cream tub package",
    "하겐다즈 스틱바 딸기": "Official product packaging studio photograph of Haagen-Dazs Strawberry Ice Cream Bar package on white background. Gourmet chocolate coated ice cream stickbar box",
    "나뚜루 파인트 녹차 474ml": "Official product packaging studio photograph of Natuur Green Tea Ice Cream Pint 474ml tub on white background. Deep green premium ice cream pint tub",
    "롯데 월드콘 바닐라 160ml": "Official product packaging studio photograph of Lotte Worldcone Vanilla Ice Cream Cone wrapper on white background. Iconic red and blue waffle cone wrapper",
    "빙그레 메로나 70ml": "Official product packaging studio photograph of Binggrae Melona Melon Ice Bar wrapper on white background. Bright pale green melon ice bar packaging wrapper",
    "해태 허니버터칩 60g": "Official product packaging studio photograph of Haitai Honey Butter Chip 60g snack bag on white background. Iconic pale yellow potato chip bag with butter graphic",
    "농심 멘토스 푸르티 37g": "Official product packaging studio photograph of Mentos Fruity 37g candy roll package on white background. Rainbow fruity candy roll package",
    "오리온 초코파이 12입 팩": "Official product packaging studio photograph of Orion Choco Pie 12pack red cardboard box on white background. Iconic red box with Korean text Jeong and choco pie photo",
    "2080 초극세모 미세모 칫솔": "Official product packaging studio photograph of 2080 Ultra Fine Toothbrush single blister pack on white background. Blue and white toothbrush packaging",
    "페리오 토탈7 알파 치약": "Official product packaging studio photograph of Perio Total 7 Alpha Toothpaste box on white background. Blue and silver toothpaste tube box package",
    "크리넥스 수프림소프트 30롤": "Official product packaging studio photograph of Kleenex Supreme Soft 30 roll toilet tissue mega pack on white background. Large plastic wrapped toilet paper 30-roll pack",
    "좋은느낌 유기농 라이너 18P": "Official product packaging studio photograph of Good Feel Organic Sanitary Liner 18P package on white background. Soft white and green feminine hygiene package",
    "가그린 제로 구강청결제 750ml": "Official product packaging studio photograph of Garglin Zero Mouthwash 750ml bottle on white background. Clear bottle with blue zero alcohol mouthwash label",
    "여명808 숙취해소음료 140ml": "Official product packaging studio photograph of Yeomyeong 808 Hangover Drink 140ml golden can on white background. Famous Korean hangover remedy golden aluminum can",
    "2080 토탈 전문 치약 120g": "Official product packaging studio photograph of Aekyung 2080 Dental Toothpaste 120g tube box package on white background. Blue toothpaste box",
    "리스테린 쿨민트 구강청결제 750ml": "Official product packaging studio photograph of Listerine Cool Mint Mouthwash 750ml bottle on white background. Iconic turquoise blue mouthwash bottle with black cap",
    "컨디션 스틱 헛개 18g": "Official product packaging studio photograph of Condition Hangover Jelly Stick 18g pouch on white background. Green and gold hangover stick jelly pouch",
    "농심 신라면 컵 65g": "Official product packaging studio photograph of Nongshim Shin Ramyun Small Cup 65g on white background. Iconic red cup noodle with black Shin character"
}

def upload_b64_to_imgbb(b64_data, filename):
    try:
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
        print(f"Error uploading {filename}: {e}")
    return None

if __name__ == "__main__":
    print(f"Total items needing dedicated image generation & upload: {len(ITEMS_TO_GENERATE)}")
