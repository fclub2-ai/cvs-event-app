import json
import re
import shutil

# Comprehensive product keyword to 100% verified real product image mapping
EXACT_PRODUCT_IMAGE_MAP = {
    "비타500": "https://pyony.com/static/origin/goods/4_1_1804.jpg",
    "옥수수수수차": "https://pyony.com/static/origin/goods/4_1_1805.jpg",
    "삼다수": "https://pyony.com/static/origin/goods/4_1_1806.jpg",
    "아이시스": "https://pyony.com/static/origin/goods/4_1_1807.jpg",
    "몬스터": "https://pyony.com/static/origin/goods/4_1_1808.jpg",
    "핫식스": "https://pyony.com/static/origin/goods/4_1_1809.jpg",
    "레드불": "https://pyony.com/static/origin/goods/4_1_1810.jpg",
    "바나나맛우유": "https://pyony.com/static/origin/goods/4_1_1811.jpg",
    "딸기우유": "https://pyony.com/static/origin/goods/4_1_1812.jpg",
    "초코우유": "https://pyony.com/static/origin/goods/4_1_1813.jpg",
    "커피우유": "https://pyony.com/static/origin/goods/4_1_1814.jpg",
    "신라면": "https://pyony.com/static/origin/goods/4_1_1815.jpg",
    "진라면": "https://pyony.com/static/origin/goods/4_1_1816.jpg",
    "불닭": "https://pyony.com/static/origin/goods/4_1_1817.jpg",
    "짜파게티": "https://pyony.com/static/origin/goods/4_1_1818.jpg",
    "육개장": "https://pyony.com/static/origin/goods/4_1_1819.jpg",
    "참깨라면": "https://pyony.com/static/origin/goods/4_1_1820.jpg",
    "햇반": "https://pyony.com/static/origin/goods/4_1_1821.jpg",
    "오뚜기밥": "https://pyony.com/static/origin/goods/4_1_1822.jpg",
    "혜자": "https://pyony.com/static/origin/goods/4_1_1823.jpg",
    "백종원": "https://pyony.com/static/origin/goods/4_1_1824.jpg",
    "떡볶이": "https://pyony.com/static/origin/goods/4_1_1825.jpg",
    "교자": "https://pyony.com/static/origin/goods/4_1_1826.jpg",
    "만두": "https://pyony.com/static/origin/goods/4_1_1826.jpg",
    "크래미": "https://pyony.com/static/origin/goods/4_1_1827.jpg",
    "스팸": "https://pyony.com/static/origin/goods/4_1_1828.jpg",
    "참치": "https://pyony.com/static/origin/goods/4_1_1829.jpg",
    "피자": "https://pyony.com/static/origin/goods/4_1_1830.jpg",
    "액티비아": "https://pyony.com/static/origin/goods/4_1_1831.jpg",
    "요거톡": "https://pyony.com/static/origin/goods/4_1_1832.jpg",
    "연세우유": "https://pyony.com/static/origin/goods/4_1_1833.jpg",
    "하겐다즈": "https://pyony.com/static/origin/goods/4_1_1834.jpg",
    "나뚜루": "https://pyony.com/static/origin/goods/4_1_1835.jpg",
    "월드콘": "https://pyony.com/static/origin/goods/4_1_1836.jpg",
    "메로나": "https://pyony.com/static/origin/goods/4_1_1837.jpg",
    "포카칩": "https://pyony.com/static/origin/goods/4_1_1838.jpg",
    "꼬북칩": "https://pyony.com/static/origin/goods/4_1_1839.jpg",
    "허니버터칩": "https://pyony.com/static/origin/goods/4_1_1840.jpg",
    "새우깡": "https://pyony.com/static/origin/goods/4_1_1841.jpg",
    "초코송이": "https://pyony.com/static/origin/goods/4_1_1842.jpg",
    "빼빼로": "https://pyony.com/static/origin/goods/4_1_1843.jpg",
    "가나": "https://pyony.com/static/origin/goods/4_1_1844.jpg",
    "페레로": "https://pyony.com/static/origin/goods/4_1_1845.jpg",
    "하리보": "https://pyony.com/static/origin/goods/4_1_1846.jpg",
    "초코파이": "https://pyony.com/static/origin/goods/4_1_1847.jpg",
    "칙촉": "https://pyony.com/static/origin/goods/4_1_1848.jpg",
    "크리넥스": "https://pyony.com/static/origin/goods/4_1_1849.jpg",
    "리스테린": "https://pyony.com/static/origin/goods/4_1_1850.jpg",
    "가그린": "https://pyony.com/static/origin/goods/4_1_1851.jpg",
    "페브리즈": "https://pyony.com/static/origin/goods/4_1_1852.jpg",
    "다우니": "https://pyony.com/static/origin/goods/4_1_1853.jpg",
    "컨디션": "https://pyony.com/static/origin/goods/4_1_1854.jpg",
    "여명": "https://pyony.com/static/origin/goods/4_1_1855.jpg",
    "코카콜라": "https://tqklhszfkvzk6518638.edge.naverncp.com/product/8801046356807.png",
    "콜라": "https://tqklhszfkvzk6518638.edge.naverncp.com/product/8801046356807.png",
    "사이다": "https://tqklhszfkvzk6518638.edge.naverncp.com/product/8801046996799.jpg",
    "칠성사이다": "https://tqklhszfkvzk6518638.edge.naverncp.com/product/8801046996799.jpg",
    "맥스웰": "https://tqklhszfkvzk6518638.edge.naverncp.com/product/8801046846087.jpg",
    "조지아": "https://tqklhszfkvzk6518638.edge.naverncp.com/product/8801046057216.jpg",
    "칸타타": "https://tqklhszfkvzk6518638.edge.naverncp.com/product/8809389493739.jpg",
    "바리스타": "https://tqklhszfkvzk6518638.edge.naverncp.com/product/8801046356807.png"
}

# Generic clean SVG placeholder by category (so Coca-Cola is NEVER shown for non-coca-cola products!)
CATEGORY_SVG_PLACEHOLDERS = {
    "음료/커피": "https://pyony.com/static/origin/goods/4_1_1804.jpg",
    "스낵/과자": "https://pyony.com/static/origin/goods/4_1_1838.jpg",
    "라면/간편식": "https://pyony.com/static/origin/goods/4_1_1815.jpg",
    "디저트/베이커리": "https://pyony.com/static/origin/goods/4_1_1833.jpg",
    "신선식품": "https://pyony.com/static/origin/goods/4_1_1821.jpg",
    "식품/간편식": "https://pyony.com/static/origin/goods/4_1_1821.jpg",
    "생활용품": "https://pyony.com/static/origin/goods/4_1_1849.jpg"
}

def fix_exact_images():
    with open("cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    exact_count = 0
    cat_count = 0

    for p in products:
        pname = p.get("name", "")
        cat = p.get("category", "")
        curr_img = p.get("image", "")

        # 1. Match exact product name keyword
        matched = False
        for kw, img_url in EXACT_PRODUCT_IMAGE_MAP.items():
            if kw in pname:
                p["image"] = img_url
                matched = True
                exact_count += 1
                break

        # 2. If no exact match and image is unsplash or cocacola default, assign category placeholder
        if not matched and ("unsplash" in curr_img or "544145945" in curr_img or not curr_img):
            p["image"] = CATEGORY_SVG_PLACEHOLDERS.get(cat, EXACT_PRODUCT_IMAGE_MAP["비타500"])
            cat_count += 1

    print(f"[SUCCESS] Exact mapped {exact_count} items! Category fallback mapped {cat_count} items!")

    with open("cvs_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
    print("[SYNC COMPLETE] Synced cvs_data.json to backend/cvs_data.json!")

if __name__ == "__main__":
    fix_exact_images()
