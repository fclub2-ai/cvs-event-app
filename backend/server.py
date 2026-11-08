"""
편의점 행사 상품 & 모의 실시간 재고 REST API 서버
- Python 표준 라이브러리(http.server) 기반 (별도 pip 설치 없이 즉시 실행 가능)
- 제공 API:
  - GET /api/events: 1+1/2+1 행사 상품 목록 (검색, 브랜드/카테고리 필터, 가성비 정렬)
  - GET /api/stores: 내 위치 주변 매장 리스트 & 실시간 모의 재고 요약
  - GET /api/stores/<id>: 특정 매장의 모의 실시간 POS 재고 상세 조회
  - GET /api/meta: 메타데이터 및 브랜드/카테고리 정보
"""

import json
import os
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "cvs_data.json")

def load_dataset():
    if not os.path.exists(DATA_FILE):
        import crawler
        return crawler.process_and_normalize_data()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

class CVSRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        dataset = load_dataset()

        # 1. API - 메타데이터
        if path == "/api/meta":
            self._set_headers(200)
            res = {
                "metadata": dataset.get("metadata", {}),
                "brands": dataset.get("brands", {}),
                "categories": dataset.get("categories", [])
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            return

        # 2. API - 행사 상품 리스트 (검색, 필터, 정렬)
        elif path == "/api/events":
            products = dataset.get("products", [])
            
            # 브랜드 필터
            brand = query_params.get("brand", [None])[0]
            if brand and brand != "ALL":
                products = [p for p in products if p["brand"].upper() == brand.upper()]

            # 카테고리 필터
            category = query_params.get("category", [None])[0]
            if category and category != "ALL":
                products = [p for p in products if p["category"] == category]

            # 행사 유형 필터 (1+1, 2+1)
            event_type = query_params.get("event_type", [None])[0]
            if event_type and event_type != "ALL":
                products = [p for p in products if p["event_type"] == event_type]

            # 검색어 (상품명)
            q = query_params.get("q", [None])[0]
            if q:
                q = q.strip().lower()
                products = [p for p in products if q in p["name"].lower()]

            # 정렬
            sort_by = query_params.get("sort", ["unit_price_asc"])[0]
            if sort_by == "unit_price_asc": # 1개당 단가 낮은순 (가성비순)
                products.sort(key=lambda x: x["unit_price"])
            elif sort_by == "discount_desc": # 할인율 높은순
                products.sort(key=lambda x: x["discount_rate"], reverse=True)
            elif sort_by == "price_asc": # 정가 낮은순
                products.sort(key=lambda x: x["price"])
            elif sort_by == "price_desc": # 정가 높은순
                products.sort(key=lambda x: x["price"], reverse=True)

            self._set_headers(200)
            res = {
                "total": len(products),
                "products": products
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            return

        # 3. API - 매장 및 모의 실시간 재고 조회
        elif path == "/api/stores":
            stores = dataset.get("stores", [])
            
            brand = query_params.get("brand", [None])[0]
            if brand and brand != "ALL":
                stores = [s for s in stores if s["brand"].upper() == brand.upper()]

            self._set_headers(200)
            res = {
                "total": len(stores),
                "stores": stores
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            return

        # 4. API - 특정 매장 상세 조회
        elif path.startswith("/api/stores/"):
            store_id = path.replace("/api/stores/", "").strip()
            stores = dataset.get("stores", [])
            target_store = next((s for s in stores if s["id"] == store_id), None)

            if target_store:
                self._set_headers(200)
                self.wfile.write(json.dumps(target_store, ensure_ascii=False).encode("utf-8"))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Store not found"}, ensure_ascii=False).encode("utf-8"))
            return

        # 알 수 없는 경로
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}, ensure_ascii=False).encode("utf-8"))

def run_server(port=8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, CVSRequestHandler)
    print(f"[OK] CVS Event & Inventory REST API Server running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
