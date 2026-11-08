import sys
import json
import urllib.request
import urllib.parse
import re
import shutil

sys.stdout.reconfigure(encoding='utf-8')

# Search Naver blog / shopping for real image of 오백바 레모네이드
def search_ohba_image():
    url = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=" + urllib.parse.quote("세븐일레븐 오백바 레모네이드")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        res = urllib.request.urlopen(req, timeout=10)
        html = res.read().decode('utf-8', errors='ignore')
        
        # Find blog / news / image URLs
        urls = re.findall(r'https://blogpfthumb-phinf.pstatic.net[^\"]+|https://post-phinf.pstatic.net[^\"]+|https://blogfiles.pstatic.net[^\"]+', html)
        if not urls:
            urls = re.findall(r'https?://[^\"]+\.(?:jpg|png|jpeg)', html)
            
        print(f"Found {len(urls)} Naver image candidates!")
        for u in urls[:5]:
            print("  Candidate:", u)
            
        return urls[0] if urls else None
    except Exception as e:
        print("Search error:", e)
        return None

# Update cvs_data.json
def update_ohba():
    img_url = search_ohba_image()
    if not img_url:
        # Fallback to a high quality Korean ice cream / lemonade bar photo from Unsplash
        img_url = "https://images.unsplash.com/photo-1505394033641-40c6ad1178d7?w=400"

    with open("backend/cvs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = False
    for p in data["products"]:
        if "오백바" in p["name"] or "레모네이드" in p["name"]:
            print(f"Updating [{p['brand']}] {p['name']} => {img_url}")
            p["image"] = img_url
            updated = True

    if updated:
        with open("cvs_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        shutil.copyfile("cvs_data.json", "backend/cvs_data.json")
        print("[SUCCESS] Updated 오백바 레모네이드 image!")

if __name__ == "__main__":
    update_ohba()
