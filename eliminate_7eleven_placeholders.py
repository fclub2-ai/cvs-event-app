import sys
import json
import re
import shutil

sys.stdout.reconfigure(encoding='utf-8')

# Clean brand/category SVG badge thumbnail for fallback
SEVEN_BRAND_FALLBACK = "https://pyony.com/static/origin/goods/4_1_1806.jpg"

def clean_token(text):
    text = re.sub(r"^(7P|7ELEVEN|CU|GS25|EMART24|CJ|PB|MDS)\)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\d+(\.\d+)?(g|g\*|ml|l|입|개|팩)", "", text, flags=re.IGNORECASE)
    tokens = re.findall(r"[가-힣a-zA-Z0-9]+", text)
    return [t for t in tokens if len(t) > 1 or t in ["컵", "면", "밥", "우유"]]

def fix_all_seven_eleven_placeholders():
    with open("backend/cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])

    # Build a dictionary of clean real packaging image URLs
    real_image_map = {}
    for p in products:
        img = p.get("image", "")
        if img and not img.endswith("product_list_01.jpg") and not img.endswith("no_image.png") and not img.endswith("1806.jpg"):
            tokens = clean_token(p["name"])
            if tokens:
                key = "".join(tokens)
                if key not in real_image_map:
                    real_image_map[key] = img
                for t in tokens:
                    if len(t) >= 2 and t not in real_image_map:
                        real_image_map[t] = img

    replaced_real = 0
    replaced_badge = 0

    for p in products:
        img = p.get("image", "")
        if "product_list_01.jpg" in img or "no_image" in img:
            tokens = clean_token(p["name"])
            matched_img = None
            
            if tokens:
                full_key = "".join(tokens)
                matched_img = real_image_map.get(full_key)
                
            if not matched_img and tokens:
                for t in tokens:
                    if len(t) >= 2 and t in real_image_map:
                        matched_img = real_image_map[t]
                        break
                        
            if matched_img:
                p["image"] = matched_img
                replaced_real += 1
            else:
                p["image"] = SEVEN_BRAND_FALLBACK
                replaced_badge += 1

    print(f"[REPLACE SUCCESS] Replaced {replaced_real} placeholders with real packaging photos!")
    print(f"[CLEAN BADGE] Replaced {replaced_badge} remaining placeholders with clean 7-Eleven brand badge!")

    with open("cvs_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
    print("[SYNC COMPLETE] Synced cvs_data.json and backend/cvs_data.json!")

if __name__ == "__main__":
    fix_all_seven_eleven_placeholders()
