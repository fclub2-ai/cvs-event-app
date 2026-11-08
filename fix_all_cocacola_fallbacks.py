import sys
import json
import re
import shutil

sys.stdout.reconfigure(encoding='utf-8')

# Clean neutral brand SVG placeholder (NO Coca-Cola!)
NEUTRAL_PLACEHOLDERS = {
    "GS25": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=300",
    "CU": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=300",
    "7-ELEVEN": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=300",
    "EMART24": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=300"
}

def clean_tokens(text):
    text = re.sub(r"^(7P|7ELEVEN|CU|GS25|EMART24|CJ|PB|MDS)\)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\d+(\.\d+)?(g|g\*|ml|l|입|개|팩)", "", text, flags=re.IGNORECASE)
    tokens = re.findall(r"[가-힣a-zA-Z0-9]+", text)
    return [t for t in tokens if len(t) > 1 or t in ["컵", "면", "밥", "우유"]]

def fix_all_cocacola_fallbacks():
    with open("backend/cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])

    # 1. Build a clean dictionary of REAL product packaging photos (excluding 1806.jpg and 1804.jpg)
    real_images = {}
    for p in products:
        img = p.get("image", "")
        if img and "1806.jpg" not in img and "1804.jpg" not in img and "product_list_01.jpg" not in img:
            tokens = clean_tokens(p["name"])
            if tokens:
                full_key = "".join(tokens)
                if full_key not in real_images:
                    real_images[full_key] = img
                for t in tokens:
                    if len(t) >= 2 and t not in real_images:
                        real_images[t] = img

    matched_real_count = 0
    neutral_replaced_count = 0

    for p in products:
        img = p.get("image", "")
        # If it has 1806.jpg (Coca-Cola), 1804.jpg (Vita500), or product_list_01.jpg
        if "1806.jpg" in img or "1804.jpg" in img or "product_list_01.jpg" in img:
            tokens = clean_tokens(p["name"])
            found_img = None

            if tokens:
                full_key = "".join(tokens)
                found_img = real_images.get(full_key)

            if not found_img and tokens:
                for t in tokens:
                    if len(t) >= 2 and t in real_images:
                        found_img = real_images[t]
                        break

            if found_img:
                p["image"] = found_img
                matched_real_count += 1
            else:
                # Use category/brand neutral SVG/thumbnail, NEVER Coca-Cola!
                p["image"] = NEUTRAL_PLACEHOLDERS.get(p["brand"], NEUTRAL_PLACEHOLDERS["7-ELEVEN"])
                neutral_replaced_count += 1

    print(f"[REPLACE SUCCESS] Replaced {matched_real_count} items with real packaging photos!")
    print(f"[NEUTRAL SUCCESS] Replaced {neutral_replaced_count} remaining items with clean neutral placeholders!")

    # Verify no 1806.jpg remains
    remaining_cocacola = sum(1 for p in products if "1806.jpg" in p.get("image", ""))
    print(f"[VERIFY] Remaining 1806.jpg (Coca-Cola) fallbacks: {remaining_cocacola}")

    with open("cvs_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
    print("[SYNC COMPLETE] Synced cvs_data.json and backend/cvs_data.json!")

if __name__ == "__main__":
    fix_all_cocacola_fallbacks()
