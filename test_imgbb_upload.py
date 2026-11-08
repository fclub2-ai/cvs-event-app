import urllib.request
import urllib.parse
import json
import base64

API_KEY = "c24ac8dace32780ff180b4b6e96cf4b0"

def upload_image_to_imgbb(image_url_or_bytes, name="product"):
    try:
        if isinstance(image_url_or_bytes, str):
            req = urllib.request.Request(
                image_url_or_bytes, 
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            img_data = urllib.request.urlopen(req, timeout=10).read()
        else:
            img_data = image_url_or_bytes

        b64_data = base64.b64encode(img_data).decode("utf-8")
        post_data = urllib.parse.urlencode({
            "key": API_KEY,
            "image": b64_data,
            "name": name
        }).encode("utf-8")

        post_req = urllib.request.Request(
            "https://api.imgbb.com/1/upload",
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        res = urllib.request.urlopen(post_req, timeout=15).read().decode("utf-8")
        res_json = json.loads(res)
        if res_json.get("success"):
            return res_json["data"]["url"]
        else:
            print("ImgBB upload failed:", res_json)
            return None
    except Exception as e:
        print(f"Error uploading {name}: {e}")
        return None

if __name__ == "__main__":
    # Test uploading Samdasoo 2L image
    test_img = "https://static.megamart.com/product/image/1357/13572655/13572655_1_960.jpg"
    uploaded = upload_image_to_imgbb(test_img, "samdasoo_test")
    print("Uploaded ImgBB URL:", uploaded)
