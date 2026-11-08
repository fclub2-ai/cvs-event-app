"""
CVS-FINDER Self-Contained Bundle Generator (v3.0 UI & KakaoMap Fix Edition)
"""
import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
APP_PATH = os.path.join(BASE_DIR, "src", "app.js")
CSS_PATH = os.path.join(BASE_DIR, "style.css")
DATA_PATH = os.path.join(BASE_DIR, "backend", "cvs_data.json")

# [핵심 패치 1] 이미지 배경 순백색 통일 + 비율 유지(contain) + 7-ELEVEN 뱃지 시인성 + 카카오맵 높이 보장 CSS
UI_FIX_CSS = """
/* === CVS-FINDER UI & THUMBNAIL STUDIO FIX === */
.product-card, .card, .item-card {
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
}

/* 1. 모든 상품 이미지 컨테이너를 순백색(#FFFFFF) 스튜디오 배경으로 통일 & 고정 높이 부여 */
.product-img-wrapper, .product-image, .card-img, .img-box, .thumb-box,
.product-card > div:first-child {
  background-color: #ffffff !important;
  height: 190px !important;
  min-height: 190px !important;
  max-height: 190px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 16px !important;
  position: relative !important;
  overflow: hidden !important;
  border-top-left-radius: inherit;
  border-top-right-radius: inherit;
}

/* 2. 사진이 너무 커지거나 잘리지 않도록 contain 강제 적용 */
.product-card img, .card img, .item-card img {
  width: 100% !important;
  height: 100% !important;
  max-width: 155px !important;
  max-height: 155px !important;
  object-fit: contain !important;
  object-position: center !important;
  background-color: #ffffff !important;
  transition: transform 0.25s ease !important;
}

.product-card:hover img {
  transform: scale(1.06) !important;
}

/* 3. 흰색 배경 위에서도 선명하게 보이도록 브랜드 뱃지 색상 & 그림자 보강 */
.badge, .brand-badge, [class*="badge"] {
  z-index: 5 !important;
  font-weight: 800 !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.18) !important;
}

/* 4. 카카오맵 컨테이너 깨짐 방지 (최소 높이 강제 확보) */
#map, #kakao-map, .map-container, .map-box {
  width: 100% !important;
  min-height: 420px !important;
  height: 420px !important;
  border-radius: 14px !important;
  overflow: hidden !important;
  background: #1e293b !important;
  position: relative !important;
  z-index: 1 !important;
}
"""

# [핵심 패치 2] 깨진 이미지/세븐일레븐 준비중 이미지 감지 + 브랜드 뱃지 컬러 보정 + 양방향 딥링크 + 카카오맵 강제 리레이아웃
RUNTIME_FIX_JS = """
(function() {
  // 1. 브랜드별 깔끔한 SVG 대체 이미지 생성기
  function createFallbackSvg(brand, title) {
    const colors = {
      'CU': '#652f8d',
      'GS25': '#007cff',
      '7-ELEVEN': '#008061',
      'SEVEN': '#008061',
      'EMART24': '#ffb81c'
    };
    const bKey = (brand || 'CVS').toUpperCase();
    const bg = colors[bKey] || '#475569';
    const safeTitle = (title || '행사 상품').substring(0, 10);
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
      <rect width="200" height="200" fill="#ffffff"/>
      <rect x="25" y="35" width="150" height="130" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
      <rect x="55" y="60" width="90" height="28" rx="6" fill="${bg}"/>
      <text x="100" y="79" font-family="sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">${bKey}</text>
      <text x="100" y="118" font-family="sans-serif" font-size="12" font-weight="bold" fill="#334155" text-anchor="middle">${safeTitle}</text>
      <text x="100" y="138" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">이미지 준비중</text>
    </svg>`;
    return 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
  }

  // 2. DOM 내 상품 이미지 & 세븐일레븐 흰색 뱃지 실시간 교정
  function enhanceProductCards() {
    // 뱃지 색상 보정 (흰 배경에 묻히는 7-ELEVEN 뱃지 등)
    document.querySelectorAll('span, div').forEach(el => {
      if (el.children.length === 0) {
        const txt = el.textContent.trim().toUpperCase();
        if (txt === '7-ELEVEN' || txt === '세븐일레븐') {
          el.style.backgroundColor = '#008061';
          el.style.color = '#ffffff';
          el.style.padding = '3px 8px';
          el.style.borderRadius = '6px';
          el.style.fontWeight = '800';
        } else if (txt === 'GS25') {
          el.style.backgroundColor = '#007cff';
          el.style.color = '#ffffff';
        }
      }
    });

    // 깨진 이미지 및 '상품 준비중입니다' 더미 이미지 교체
    document.querySelectorAll('img').forEach(img => {
      if (img.dataset.cvsFixed) return;
      img.dataset.cvsFixed = "true";
      img.setAttribute('referrerpolicy', 'no-referrer');

      const card = img.closest('.product-card, .card, .item-card') || img.parentElement?.parentElement;
      const brandText = card ? (card.innerText.match(/CU|GS25|7-ELEVEN|EMART24/i)?.[0] || 'CVS') : 'CVS';
      const titleEl = card ? card.querySelector('h3, h4, .product-name, .title, strong') : null;
      const titleText = titleEl ? titleEl.textContent.trim() : (img.alt || '행사 상품');

      const applyFallback = () => {
        img.src = createFallbackSvg(brandText, titleText);
      };

      img.addEventListener('error', applyFallback);

      const srcLower = (img.getAttribute('src') || '').toLowerCase();
      if (!srcLower || srcLower.includes('no_image') || srcLower.includes('noimage') || srcLower.includes('ready')) {
        applyFallback();
      }
    });
  }

  // 3. 카카오맵 자동 리레이아웃 & 내 위치 주변 편의점 마커 보정
  function fixKakaoMap() {
    const mapContainer = document.getElementById('map') || document.getElementById('kakao-map') || document.querySelector('.map-container');
    if (!mapContainer || typeof kakao === 'undefined' || !kakao.maps) return;

    // 기존 지도가 깨져 있거나 비어 있으면 재초기화 지원
    if (window.map && typeof window.map.relayout === 'function') {
      setTimeout(() => { window.map.relayout(); }, 250);
      return;
    }

    if (mapContainer.children.length === 0) {
      kakao.maps.load(() => {
        const defaultPos = new kakao.maps.LatLng(37.4979, 127.0276); // 기본값: 서울 강남역
        const mapOption = { center: defaultPos, level: 4 };
        const map = new kakao.maps.Map(mapContainer, mapOption);
        window.map = map;

        const ps = new kakao.maps.services ? new kakao.maps.services.Places() : null;
        const infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });

        function searchNearbyCVS(lat, lng) {
          const loc = new kakao.maps.LatLng(lat, lng);
          map.setCenter(loc);
          map.relayout();
          if (!ps) return;
          const activeBrand = (window.state && window.state.selectedBrand && window.state.selectedBrand !== 'ALL')
            ? window.state.selectedBrand.replace('7-ELEVEN', '세븐일레븐').replace('EMART24', '이마트24')
            : '편의점';
          ps.keywordSearch(activeBrand, (data, status) => {
            if (status === kakao.maps.services.Status.OK) {
              data.forEach(place => {
                const marker = new kakao.maps.Marker({
                  map: map,
                  position: new kakao.maps.LatLng(place.y, place.x)
                });
                kakao.maps.event.addListener(marker, 'click', () => {
                  infowindow.setContent(`<div style="padding:6px 10px;font-size:12px;color:#0f172a;font-weight:bold;">${place.place_name}</div>`);
                  infowindow.open(map, marker);
                });
              });
            }
          }, { location: loc, radius: 1000 });
        }

        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            pos => searchNearbyCVS(pos.coords.latitude, pos.coords.longitude),
            () => searchNearbyCVS(37.4979, 127.0276),
            { timeout: 5000 }
          );
        } else {
          searchNearbyCVS(37.4979, 127.0276);
        }
      });
    }
  }

  // DOM 변경 감시 (필터 클릭, 더보기 클릭 시 즉시 이미지/뱃지 보정)
  const observer = new MutationObserver(() => {
    enhanceProductCards();
  });

  window.addEventListener('DOMContentLoaded', () => {
    enhanceProductCards();
    setTimeout(fixKakaoMap, 500);
    observer.observe(document.body, { childList: true, subtree: true });

    // 탭이나 버튼 클릭 시 지도 깨짐 방지용 relayout 트리거
    document.body.addEventListener('click', () => {
      setTimeout(() => {
        if (window.map && typeof window.map.relayout === 'function') {
          window.map.relayout();
        }
      }, 200);
    });
  });
})();
"""

def bundle():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    with open(APP_PATH, "r", encoding="utf-8") as f:
        js = f.read()
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 기존 인라인 스크립트 및 스타일 태그 깔끔하게 제거 (무한 증식 방지)
    html = re.sub(r'<script id="embedded-data">.*?</script>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<script id="embedded-app">.*?</script>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<script id="cvs-runtime-fixer">.*?</script>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<script>\s*window\.EMBEDDED_CVS_DATA\s*=.*?</script>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<script src="src/app\.js.*?</script>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<style.*?>.*?</style>\s*', '', html, flags=re.DOTALL)

    # 2. 외부 편의점 이미지 차단(Hotlink) 우회 메타태그 주입
    if 'name="referrer"' not in html:
        html = html.replace('<head>', '<head>\n  <meta name="referrer" content="no-referrer">')

    # 3. 카카오맵 SDK에 services 라이브러리(장소 검색용) 누락 시 자동 보강
    html = re.sub(
        r'(//dapi\.kakao\.com/v2/maps/sdk\.js\?appkey=[^"&]+)(?!.*libraries=services)',
        r'\1&libraries=services',
        html
    )

    # 4. 원본 CSS + UI 교정 CSS 통합 주입
    inline_css_tag = f'<style id="inlined-style">\n{css}\n{UI_FIX_CSS}\n</style>'
    if '<link rel="stylesheet" href="style.css">' in html:
        html = html.replace('<link rel="stylesheet" href="style.css">', inline_css_tag)
    else:
        html = html.replace('</head>', f'{inline_css_tag}\n</head>')

    # 5. 총 상품 수 업데이트
    total_prods = len(data.get("products", []))
    html = re.sub(
        r'(<span class="stat-num" id="stat-total-items">)\d+(</span>)',
        rf'\g<1>{total_prods}\g<2>',
        html
    )

    # 6. 경량화 JSON 데이터 + 앱 스크립트 + 런타임 보정기 안전 주입
    js_safe = js.replace("</script>", "<\/script>")
    compact_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    embedded_scripts = (
        f'<script id="embedded-data">\nwindow.EMBEDDED_CVS_DATA = {compact_json};\n</script>\n'
        f'<script id="embedded-app">\n{js_safe}\n</script>\n'
        f'<script id="cvs-runtime-fixer">\n{RUNTIME_FIX_JS}\n</script>\n'
    )

    if "</body>" in html:
        final_html = html.replace("</body>", f"{embedded_scripts}</body>")
    else:
        final_html = html + "\n" + embedded_scripts

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"[SUCCESS] UI/Map Fixed & Bundled index.html ({len(final_html)/1024:.1f} KB)")

if __name__ == "__main__":
    bundle()
