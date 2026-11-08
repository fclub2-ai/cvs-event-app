import urllib.request
import urllib.parse
import json
import base64
import subprocess
import re

API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

def harvest_and_upload(product_name):
    encoded = urllib.parse.quote(product_name + " 누끼 상품 이미지")
    url = f"https://m.search.naver.com/search.naver?where=m_image&query={encoded}"
    cmd = [
        "curl.exe", "-s", "-L",
        "-H", "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    html = res.stdout
    imgs = re.findall(r'https://search\.pstatic\.net/[^"\'\s<>\\]+', html)
    
    # Priority for shopping/item CDNs over personal blogs
    shopping_imgs = []
    other_imgs = []
    for img in imgs:
        decoded = urllib.parse.unquote(img)
        if any(cdn in decoded for cdn in ['lotteon.com', 'ssgcdn.com', 'coupangcdn.com', '011st.com', 'shop1.phinf.naver.net', 'wemep.co.kr', 'gmarket.co.kr', 'homeplus.co.kr']):
            shopping_imgs.append(decoded)
        elif not any(x in decoded for x in ['blogpfthumb', 'type=f', 'logo', 'icon']):
            other_imgs.append(decoded)
            
    candidates = shopping_imgs + other_imgs
    if not candidates:
        print(f"No candidates found for {product_name}")
        return None
        
    target_url = candidates[0]
    print(f"[{product_name}] Target image: {target_url[:90]}...")
    
    # Download image bytes
    try:
        req = urllib.request.Request(target_url, headers={"User-Agent": "Mozilla/5.0"})
        img_bytes = urllib.request.urlopen(req, timeout=10).read()
        b64_data = base64.b64encode(img_bytes).decode("utf-8")
        
        # Upload to ImgBB
        post_data = urllib.parse.urlencode({
            "key": API_KEY,
            "image": b64_data,
            "name": product_name
        }).encode("utf-8")
        
        post_req = urllib.request.Request(
            "https://api.imgbb.com/1/upload",
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        res_upload = urllib.request.urlopen(post_req, timeout=15).read().decode("utf-8")
        res_json = json.loads(res_upload)
        if res_json.get("success"):
            imgbb_url = res_json["data"]["url"]
            print(f"  -> SUCCESS ImgBB URL: {imgbb_url}")
            return imgbb_url
        else:
            print("  -> ImgBB upload failed:", res_json)
    except Exception as e:
        print(f"  -> Error for {product_name}: {e}")
    return None

if __name__ == "__main__":
    test_items = ["코카콜라 500ml", "광동 비ta500 100ml", "농심 신라면 컵 65g", "연세우유 생크림빵 130g", "해태 허니버터칩 60g"]
    for item in test_items:
        harvest_and_upload(item)
