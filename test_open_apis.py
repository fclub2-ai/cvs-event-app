import urllib.request
import urllib.parse
import json

def search_wikimedia(query):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&format=json&prop=imageinfo&iiprop=url&gsrlimit=5"
    headers = {"User-Agent": "CvsEventApp/1.0 (contact@example.com)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(res)
        pages = data.get("query", {}).get("pages", {})
        urls = []
        for page_id, page_info in pages.items():
            imageinfo = page_info.get("imageinfo", [])
            for info in imageinfo:
                if "url" in info:
                    urls.append(info["url"])
        return urls
    except Exception as e:
        print(f"Wikimedia error for {query}: {e}")
        return []

def search_open_food_facts(query):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={urllib.parse.quote(query)}&search_simple=1&action=process&json=1&page_size=5"
    headers = {"User-Agent": "CvsEventApp/1.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(res)
        products = data.get("products", [])
        urls = []
        for p in products:
            img = p.get("image_front_url") or p.get("image_url")
            if img:
                urls.append(img)
        return urls
    except Exception as e:
        print(f"OFF error for {query}: {e}")
        return []

if __name__ == "__main__":
    products = [
        "Coca-Cola 500ml bottle", "Monster Energy 355ml can", "Red Bull 250ml can",
        "Shin Ramyun", "Nutella", "Haribo Goldbären 100g", "Pringles"
    ]
    for p in products:
        wm = search_wikimedia(p)
        off = search_open_food_facts(p)
        print(f"[{p}] Wiki: {len(wm)}, OFF: {len(off)}")
        if wm:
            print("  Wiki ->", wm[0])
        if off:
            print("  OFF  ->", off[0])
