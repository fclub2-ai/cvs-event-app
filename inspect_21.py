import json
import os

data_path = r'C:\Users\fclub\cvs-event-app\backend\cvs_data.json'
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', [])
print(f"Total products in data: {len(products)}")

targets = [
    "농심 신라면 컵 65g",
    "오뚜기 진라면 매운맛 컵",
    "삼양 불닭볶음면 큰사발",
    "농심 짜파게티 큰사발",
    "농심 육개장 사발면 86g",
    "오뚜기 참깨라면 컵",
    "CJ 햇반 210g",
    "오뚜기 오뚜기밥 210g",
    "혜자로운집밥 제육볶음도시락",
    "백종원 매콤제육 정식도시락",
    "죠스떡볶이 컵 떡볶이",
    "CJ 비비고 왕교자 만두 455g",
    "한성 크래미 90g",
    "CJ 스팸 클래식 200g",
    "동원 살코기 참치캔 150g",
    "사조 한입피자 콤비네이션 80g",
    "풀무원 액티비아업 딸기 210ml",
    "풀무원 요거톡 스타볼 132g",
    "연세우유 생크림빵 130g",
    "하겐다즈 파인트 바닐라 473ml",
    "하겐다즈 스틱바 딸기"
]

print("Matching target products in cvs_data.json:")
found_count = 0
for idx, target in enumerate(targets, 1):
    # Extract core keywords
    keywords = target.split()
    matched_items = []
    for p in products:
        p_name = p['name']
        # Check if key words match
        # E.g. for "농심 신라면 컵 65g", match "신라면" and ("컵" or "소컵" or "65g")
        if idx == 1 and ("신라면" in p_name and ("컵" in p_name or "소컵" in p_name or "65g" in p_name)):
            matched_items.append(p)
        elif idx == 2 and ("진라면" in p_name and "매운" in p_name and "컵" in p_name):
            matched_items.append(p)
        elif idx == 3 and ("불닭" in p_name and ("큰사발" in p_name or "사발" in p_name or "컵" in p_name)):
            matched_items.append(p)
        elif idx == 4 and ("짜파게티" in p_name and ("큰사발" in p_name or "사발" in p_name or "컵" in p_name)):
            matched_items.append(p)
        elif idx == 5 and ("육개장" in p_name and ("사발" in p_name or "86g" in p_name)):
            matched_items.append(p)
        elif idx == 6 and ("참깨라면" in p_name and "컵" in p_name):
            matched_items.append(p)
        elif idx == 7 and ("햇반" in p_name and "210g" in p_name):
            matched_items.append(p)
        elif idx == 8 and ("오뚜기밥" in p_name and "210g" in p_name):
            matched_items.append(p)
        elif idx == 9 and ("혜자" in p_name or "제육볶음" in p_name and "GS25" in p['brand']):
            matched_items.append(p)
        elif idx == 10 and ("백종원" in p_name or ("제육" in p_name and "CU" in p['brand'])):
            matched_items.append(p)
        elif idx == 11 and ("죠스" in p_name or "떡볶이" in p_name):
            matched_items.append(p)
        elif idx == 12 and ("비비고" in p_name or "왕교자" in p_name or "만두" in p_name):
            matched_items.append(p)
        elif idx == 13 and ("크래미" in p_name):
            matched_items.append(p)
        elif idx == 14 and ("스팸" in p_name and ("클래식" in p_name or "200g" in p_name)):
            matched_items.append(p)
        elif idx == 15 and ("참치" in p_name and ("살코기" in p_name or "150g" in p_name)):
            matched_items.append(p)
        elif idx == 16 and ("피자" in p_name or "한입피자" in p_name):
            matched_items.append(p)
        elif idx == 17 and ("액티비아" in p_name):
            matched_items.append(p)
        elif idx == 18 and ("요거톡" in p_name):
            matched_items.append(p)
        elif idx == 19 and ("연세" in p_name or "생크림빵" in p_name):
            matched_items.append(p)
        elif idx == 20 and ("하겐다즈" in p_name and "바닐라" in p_name):
            matched_items.append(p)
        elif idx == 21 and ("하겐다즈" in p_name and ("스틱바" in p_name or "딸기" in p_name or "바" in p_name)):
            matched_items.append(p)

    print(f"[{idx}] {target}: {len(matched_items)} items matched -> {[m['name'] for m in matched_items]}")
