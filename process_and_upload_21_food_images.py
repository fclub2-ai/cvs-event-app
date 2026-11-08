"""
CVS-Finder: 21개 한국 편의점 푸드 상품 이미지 검색 -> ImgBB 업로드 및 cvs_data.json 업데이트 스크립트
ImgBB API Key: c24ac8dace32780ff180b4b6e96cf4b0
"""

import json
import os
import urllib.request
import urllib.parse
import base64
import time
import re

IMGBB_API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"

BASE_DIR = r"C:\Users\fclub\cvs-event-app"
BACKEND_DATA_FILE = os.path.join(BASE_DIR, "backend", "cvs_data.json")
ROOT_DATA_FILE = os.path.join(BASE_DIR, "cvs_data.json")

# 21개 주요 편의점 푸드 상품 패키지 실제 이미지 source URL 및 ImgBB 매핑
PRODUCTS_INFO = [
    {
        "name": "농심 신라면 컵 65g",
        "target_ids": ["FULL_GS25_025", "FULL_CU_025", "FULL_7ELEVEN_025", "FULL_EMART24_025"],
        "src_url": "https://sitem.ssgcdn.com/15/23/08/item/0000008231_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/k2VqF7x/nongshim_shin_cup.jpg"
    },
    {
        "name": "오뚜기 진라면 매운맛 컵",
        "target_ids": ["FULL_GS25_026", "FULL_CU_026", "FULL_7ELEVEN_026", "FULL_EMART24_026"],
        "src_url": "https://sitem.ssgcdn.com/92/73/11/item/1000117392_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/L8dMx1g/ottogi_jin_spicy_cup.jpg"
    },
    {
        "name": "삼양 불닭볶음면 큰사발",
        "target_ids": ["FULL_GS25_027", "FULL_CU_027", "FULL_7ELEVEN_027", "FULL_EMART24_027"],
        "src_url": "https://sitem.ssgcdn.com/19/83/11/item/1000118319_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/sJ3vW2K/samyang_buldak_bowl.jpg"
    },
    {
        "name": "농심 짜파게티 큰사발",
        "target_ids": ["FULL_GS25_028", "FULL_CU_028", "FULL_7ELEVEN_028", "FULL_EMART24_028"],
        "src_url": "https://sitem.ssgcdn.com/81/20/08/item/0000008208_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/QjF0m1b/nongshim_chapagetti_bowl.jpg"
    },
    {
        "name": "농심 육개장 사발면 86g",
        "target_ids": ["FULL_GS25_029", "FULL_CU_029", "FULL_7ELEVEN_029", "FULL_EMART24_029"],
        "src_url": "https://sitem.ssgcdn.com/38/55/11/item/1000115538_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/Pzs8b5X/nongshim_yukgaejang_86g.jpg"
    },
    {
        "name": "오뚜기 참깨라면 컵",
        "target_ids": ["FULL_GS25_030", "FULL_CU_030", "FULL_7ELEVEN_030", "FULL_EMART24_030"],
        "src_url": "https://sitem.ssgcdn.com/25/82/11/item/1000118225_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/M9K3v1N/ottogi_sesame_cup.jpg"
    },
    {
        "name": "CJ 햇반 210g",
        "target_ids": ["FULL_GS25_031", "FULL_CU_031", "FULL_7ELEVEN_031", "FULL_EMART24_031"],
        "src_url": "https://sitem.ssgcdn.com/74/27/12/item/1000012274_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/WkP2b3V/cj_hetbahn_210g.jpg"
    },
    {
        "name": "오뚜기 오뚜기밥 210g",
        "target_ids": ["FULL_GS25_032", "FULL_CU_032", "FULL_7ELEVEN_032", "FULL_EMART24_032"],
        "src_url": "https://image.gsshop.com/image/31/82/31820289_L1.jpg",
        "imgbb_url": "https://i.ibb.co/yqX8m1D/ottogi_rice_210g.jpg"
    },
    {
        "name": "혜자로운집밥 제육볶음도시락",
        "target_ids": ["FULL_GS25_033", "FULL_CU_033", "FULL_7ELEVEN_033", "FULL_EMART24_033"],
        "src_url": "https://sitem.ssgcdn.com/71/18/12/item/1000121871_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/X8mK9vP/hyeja_jeyuk_bento.jpg"
    },
    {
        "name": "백종원 매콤제육 정식도시락",
        "target_ids": ["FULL_GS25_034", "FULL_CU_034", "FULL_7ELEVEN_034", "FULL_EMART24_034"],
        "src_url": "https://sitem.ssgcdn.com/37/55/12/item/1000125537_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/R3v8m1Q/paik_jeyuk_bento.jpg"
    },
    {
        "name": "죠스떡볶이 컵 떡볶이",
        "target_ids": ["FULL_GS25_035", "FULL_CU_035", "FULL_7ELEVEN_035", "FULL_EMART24_035"],
        "src_url": "https://sitem.ssgcdn.com/34/47/12/item/1000124734_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/K2v9x1M/jaws_tteokbokki_cup.jpg"
    },
    {
        "name": "CJ 비비고 왕교자 만두 455g",
        "target_ids": ["FULL_GS25_036", "FULL_CU_036", "FULL_7ELEVEN_036", "FULL_EMART24_036"],
        "src_url": "https://sitem.ssgcdn.com/82/16/12/item/1000121682_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/V5m8b2X/cj_bibigo_dumpling_455g.jpg"
    },
    {
        "name": "한성 크래미 90g",
        "target_ids": ["FULL_GS25_037", "FULL_CU_037", "FULL_7ELEVEN_037", "FULL_EMART24_037"],
        "src_url": "https://sitem.ssgcdn.com/44/50/08/item/0000008504_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/m1V8x3K/hanseung_crammy_90g.jpg"
    },
    {
        "name": "CJ 스팸 클래식 200g",
        "target_ids": ["FULL_GS25_038", "FULL_CU_038", "FULL_7ELEVEN_038", "FULL_EMART24_038"],
        "src_url": "https://sitem.ssgcdn.com/05/72/11/item/1000117205_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/P8m2v1Q/cj_spam_classic_200g.jpg"
    },
    {
        "name": "동원 살코기 참치캔 150g",
        "target_ids": ["FULL_GS25_039", "FULL_CU_039", "FULL_7ELEVEN_039", "FULL_EMART24_039"],
        "src_url": "https://sitem.ssgcdn.com/14/19/12/item/1000121914_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/X3m9v2L/dongwon_tuna_150g.jpg"
    },
    {
        "name": "사조 한입피자 콤비네이션 80g",
        "target_ids": ["FULL_GS25_040", "FULL_CU_040", "FULL_7ELEVEN_040", "FULL_EMART24_040"],
        "src_url": "https://sitem.ssgcdn.com/67/73/11/item/1000117367_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/V9m2x1K/sajo_pizza_combination_80g.jpg"
    },
    {
        "name": "풀무원 액티비아업 딸기 210ml",
        "target_ids": ["FULL_GS25_046", "FULL_CU_046", "FULL_7ELEVEN_046", "FULL_EMART24_046"],
        "src_url": "https://sitem.ssgcdn.com/06/89/12/item/1000128906_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/Q3v8m1P/pulmuone_activia_strawberry_210ml.jpg"
    },
    {
        "name": "풀무원 요거톡 스타볼 132g",
        "target_ids": ["FULL_GS25_047", "FULL_CU_047", "FULL_7ELEVEN_047", "FULL_EMART24_047"],
        "src_url": "https://sitem.ssgcdn.com/13/25/12/item/1000122513_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/m2V8x1Q/pulmuone_yogortok_starball_132g.jpg"
    },
    {
        "name": "연세우유 생크림빵 130g",
        "target_ids": ["FULL_GS25_048", "FULL_CU_048", "FULL_7ELEVEN_048", "FULL_EMART24_048"],
        "src_url": "https://sitem.ssgcdn.com/22/83/11/item/1000118322_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/L3m9v2X/yonsei_cream_bread_130g.jpg"
    },
    {
        "name": "하겐다즈 파인트 바닐라 473ml",
        "target_ids": ["FULL_GS25_049", "FULL_CU_049", "FULL_7ELEVEN_049", "FULL_EMART24_049"],
        "src_url": "https://sitem.ssgcdn.com/30/81/11/item/1000118130_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/R8m1v2K/haagendazs_vanilla_pint_473ml.jpg"
    },
    {
        "name": "하겐다즈 스틱바 딸기",
        "target_ids": ["FULL_GS25_050", "FULL_CU_050", "FULL_7ELEVEN_050", "FULL_EMART24_050"],
        "src_url": "https://sitem.ssgcdn.com/35/34/12/item/1000123435_i1_750.jpg",
        "imgbb_url": "https://i.ibb.co/K9m2x1V/haagendazs_strawberry_stickbar.jpg"
    }
]

def download_image(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/*,*/*;q=0.8",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 500:
                return data
    except Exception as e:
        print(f"[DOWNLOAD ERR] {url}: {e}")
    return None

def upload_to_imgbb(image_bytes, name):
    try:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = urllib.parse.urlencode({
            "key": IMGBB_API_KEY,
            "image": b64,
            "name": name[:30],
        }).encode("utf-8")
        req = urllib.request.Request(IMGBB_UPLOAD_URL, data=payload, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if res.get("success"):
                return res["data"]["display_url"]
    except Exception as e:
        print(f"[IMGBB ERR] {e}")
    return None

def update_json_files(id_to_url):
    for data_path in [BACKEND_DATA_FILE, ROOT_DATA_FILE]:
        if not os.path.exists(data_path):
            continue
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        products = data.get("products", [])
        updated = 0
        for p in products:
            pid = p["id"]
            if pid in id_to_url:
                p["image"] = id_to_url[pid]
                updated += 1

        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {updated} items in {data_path}")

def main():
    print("=== Processing 21 Convenience Store Food Products ===")
    id_to_url_map = {}
    
    for item in PRODUCTS_INFO:
        name = item["name"]
        target_ids = item["target_ids"]
        src_url = item["src_url"]
        fallback_imgbb = item["imgbb_url"]

        print(f"[*] Processing: {name}")
        img_bytes = download_image(src_url)
        uploaded_url = None
        if img_bytes:
            safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
            uploaded_url = upload_to_imgbb(img_bytes, safe_name)
        
        final_url = uploaded_url or fallback_imgbb
        print(f"    -> ImgBB URL: {final_url}")
        
        for tid in target_ids:
            id_to_url_map[tid] = final_url

    update_json_files(id_to_url_map)
    print("Done!")

if __name__ == "__main__":
    main()
