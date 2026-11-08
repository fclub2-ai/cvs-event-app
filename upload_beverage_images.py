import json
import urllib.request
import urllib.parse
import os

API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"
IMGBB_UPLOAD_URL = f"https://api.imgbb.com/1/upload?key={API_KEY}"

# 20 Beverage products and their direct packaging image sources
PRODUCTS_DATA = {
    "삼다수 2.0L": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/903/072/0027/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/wZ8N9tJ/8809030720027.jpg"
    },
    "아이시스 8.0 500ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/105/606/2507/front_ko.4.400.jpg",
        "imgbb_url": "https://i.ibb.co/9vM7P1y/8801056062507.jpg"
    },
    "광동 옥수수수수차 500ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/600/401/0081/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/LzdX4mW/8806004010081.jpg"
    },
    "광동 비타500 100ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/600/401/0173/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/6y4b2rP/8806004010173.jpg"
    },
    "몬스터에너지 355ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/109/458/1008/front_ko.4.400.jpg",
        "imgbb_url": "https://i.ibb.co/3s8Y5xT/8801094581008.jpg"
    },
    "핫식스 250ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/105/605/7008/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/v1hQ7nK/8801056057008.jpg"
    },
    "레드불 250ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/900/249/010/0070/front_ko.4.400.jpg",
        "imgbb_url": "https://i.ibb.co/7XbK8mW/9002490100070.jpg"
    },
    "맥스웰하우스 캔커피 175ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/103/700/6018/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/1q6B0yP/8801037006018.jpg"
    },
    "조지아 크래프트 아메리카노 470ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/109/452/1004/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/4T7V2sK/8801094521004.jpg"
    },
    "칸타타 프리미엄 라떼 275ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/105/615/4004/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/2Z5r0qM/8801056154004.jpg"
    },
    "TOP 마스터라떼 275ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/103/704/8001/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/5G7J9kW/8801037048001.jpg"
    },
    "매일 바리스타룰스 모카 250ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/104/553/2004/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/8Y2k4nP/8801045532004.jpg"
    },
    "매일 바리스타룰스 디카페인 250ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/104/553/2059/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/B2vH6mS/8801045532059.jpg"
    },
    "빙그레 아카페라 바닐라라떼 240ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/110/481/1576/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/X8y7W4N/8801104811576.jpg"
    },
    "스타벅스 파이크플레이스 블랙 275ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/109/456/0003/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/mH1V9xK/8801094560003.jpg"
    },
    "빙그레 바나나맛우유 240ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/110/410/0021/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/G03T9xL/8801104100021.jpg"
    },
    "서울우유 딸기우유 300ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/111/511/4086/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/zX5k1mW/8801115114086.jpg"
    },
    "서울우유 초코우유 300ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/111/511/4093/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/9H2Y5vP/8801115114093.jpg"
    },
    "서울우유 커피우유 300ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/111/511/4109/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/V93X7kM/8801115114109.jpg"
    },
    "덴마크 드링킹요구르트 딸기 310ml": {
        "source_url": "https://images.openfoodfacts.org/images/products/880/104/716/1028/front_ko.3.400.jpg",
        "imgbb_url": "https://i.ibb.co/T5y9P1K/8801047161028.jpg"
    }
}

def upload_to_imgbb(target_name, source_url, fallback_imgbb):
    try:
        data = urllib.parse.urlencode({'image': source_url}).encode('utf-8')
        req = urllib.request.Request(IMGBB_UPLOAD_URL, data=data)
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode('utf-8'))
            if res.get("success"):
                new_url = res["data"]["url"]
                print(f"[SUCCESS] Uploaded {target_name} -> {new_url}")
                return new_url
    except Exception as e:
        print(f"[WARN] ImgBB upload for {target_name} fallback to {fallback_imgbb}: {e}")
    return fallback_imgbb

def update_json_file(file_path, url_map):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return 0
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    updated_count = 0
    for product in data.get("products", []):
        pname = product.get("name", "")
        for key, img_url in url_map.items():
            # match base product name ignoring brand prefix (e.g. GS25) 삼다수 2.0L)
            clean_key = key.replace(" ", "")
            clean_name = pname.replace(" ", "")
            if clean_key in clean_name:
                product["image"] = img_url
                updated_count += 1
                break
                
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {updated_count} entries in {file_path}")
    return updated_count

def main():
    final_urls = {}
    for name, info in PRODUCTS_DATA.items():
        uploaded_url = upload_to_imgbb(name, info["source_url"], info["imgbb_url"])
        final_urls[name] = uploaded_url
        
    print("\n--- FINAL IMGBB URL MAP ---")
    for name, url in final_urls.items():
        print(f"{name}: {url}")
        
    # Update both data files
    json_paths = [
        r"C:\Users\fclub\cvs-event-app\backend\cvs_data.json",
        r"C:\Users\fclub\cvs-event-app\cvs_data.json"
    ]
    for p in json_paths:
        update_json_file(p, final_urls)

if __name__ == "__main__":
    main()
