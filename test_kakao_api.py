import urllib.request
import urllib.parse
import json

KAKAO_REST_KEY = "4395d77cea7a56b51d67144e1a360cdf"

def search_kakao_images(query):
    url = f"https://dapi.kakao.com/v2/search/image?query={urllib.parse.quote(query + ' 제품')}&size=5"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"KakaoAK {KAKAO_REST_KEY}"}
    )
    try:
        res = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(res)
        documents = data.get("documents", [])
        return [doc["image_url"] for doc in documents if "image_url" in doc]
    except Exception as e:
        print(f"Kakao API error for {query}: {e}")
        return []

if __name__ == "__main__":
    products = [
        "코카콜라 500ml", "광동 비타500 100ml", "몬스터에너지 355ml", "농심 신라면 컵 65g",
        "CJ 햇반 210g", "빙그레 바나나맛우유 240ml", "하겐다즈 파인트 바닐라 473ml", "오리온 포카칩 오리지널 66g"
    ]
    for p in products:
        imgs = search_kakao_images(p)
        print(f"[{p}] Kakao API: {len(imgs)} images found")
        for img in imgs[:2]:
            print("  ->", img)
