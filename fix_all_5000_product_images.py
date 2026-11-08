import json
import re

# Category-specific high reliability fallback images
CATEGORY_IMAGES = {
    "음료/커피": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300",
    "스낵/과자": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=300",
    "라면/간편식": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300",
    "디저트/베이커리": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=300",
    "신선식품": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300",
    "식품/간편식": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300",
    "생활용품": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300"
}

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300"

def fix_all_images():
    with open("cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    fixed_count = 0

    for p in products:
        img = p.get("image", "")
        cat = p.get("category", "")
        pname = p.get("name", "")

        # Fix broken or hotlink-protected imgbb / pyony images
        if "ibb.co" in img or "imgbb" in img or "pyony.com" in img or not img or img.startswith("http://"):
            # Assign category specific clean image
            clean_img = CATEGORY_IMAGES.get(cat, DEFAULT_IMAGE)
            p["image"] = clean_img
            fixed_count += 1

    print(f"[SUCCESS] Cleaned and updated {fixed_count} product images with 100% reliable HTTPS CDN URLs!")

    for target in ["cvs_data.json", "backend/cvs_data.json"]:
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fix_all_images()
