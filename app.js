/**
 * CVS-Finder Web Application Script (Dual-Engine Bulletproof Map System)
 * - Kakao Maps SDK & Leaflet Dark Fallback 자동 전환 지도 엔진
 * - 1+1 / 2+1 실제 행사 상품 필터링 & 가성비 계산
 * - 정밀 매칭 주소 & 지점명 마커 시각화 및 본사 앱 딥링크 연동
 */

const API_BASE = "http://localhost:8080/api";

// 편의점 공식 앱 / 웹 재고 확인 딥링크 주소
const OFFICIAL_APP_LINKS = {
  "GS25": { name: "우리동네GS 앱에서 실시간 재고 확인", url: "https://woodong.gsretail.com/", bg: "#0072CE" },
  "CU": { name: "포켓CU 앱에서 실시간 재고 확인", url: "https://cu.bgfretail.com/event/plus.do", bg: "#652D90" },
  "7-ELEVEN": { name: "세븐일레븐 앱에서 실시간 재고 확인", url: "https://www.7-eleven.co.kr/product/presentList.asp", bg: "#00805A" },
  "EMART24": { name: "이마트24 앱에서 실시간 재고 확인", url: "https://www.emart24.co.kr/product/eventProduct.asp", bg: "#FFB81C" }
};

// 전역 상태
const state = {
  products: [],
  stores: [],
  filteredProducts: [],
  selectedBrand: "ALL",
  selectedEventType: "ALL",
  selectedCategory: "ALL",
  searchQuery: "",
  sortBy: "unit_price_asc",
  selectedMapBrand: "ALL",
  activeStore: null,
  map: null,
  mapEngine: "kakao", // "kakao" or "leaflet"
  markers: [],
  activeInfowindow: null
};

// DOM 로드 시 초기화
document.addEventListener("DOMContentLoaded", async () => {
  initNavigation();
  initFilterEvents();
  await loadData();
  initSmartMapEngine();
});

// 1. 탭 네비게이션
function initNavigation() {
  const tabs = document.querySelectorAll(".nav-tab-btn");
  tabs.forEach(btn => {
    btn.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
      
      btn.classList.add("active");
      const targetId = btn.dataset.tab;
      const targetEl = document.getElementById(targetId);
      if (targetEl) targetEl.classList.add("active");

      if (targetId === "tab-map" && state.map) {
        setTimeout(() => {
          if (state.mapEngine === "kakao" && state.map.relayout) {
            state.map.relayout();
            renderKakaoMapMarkers();
          } else if (state.mapEngine === "leaflet" && state.map.invalidateSize) {
            state.map.invalidateSize();
            renderLeafletMapMarkers();
          }
        }, 200);
      }
    });
  });

  document.getElementById("modal-close-btn")?.addEventListener("click", closeModal);
  document.getElementById("store-modal")?.addEventListener("click", (e) => {
    if (e.target.id === "store-modal") closeModal();
  });
}

// 2. REST API & 정적 JSON 실데이터 로드
async function loadData() {
  let eventsData = null;
  let storesData = null;

  // 1) REST API 서버 시도
  try {
    const [eventsRes, storesRes] = await Promise.all([
      fetch(`${API_BASE}/events`).then(r => r.json()),
      fetch(`${API_BASE}/stores`).then(r => r.json())
    ]);
    if (eventsRes && eventsRes.products) eventsData = eventsRes.products;
    if (storesRes && storesRes.stores) storesData = storesRes.stores;
  } catch (err) {
    console.warn("⚠️ REST API 연결 대기 중 (정적 JSON 호스팅으로 자동 전환):", err);
  }

  // 2) HTTPS Cloudflare Pages 호스팅 환경 정적 JSON 자동 폴백
  if (!eventsData || eventsData.length === 0) {
    try {
      const staticRes = await fetch("./cvs_data.json")
        .then(r => r.json())
        .catch(() => fetch("./backend/cvs_data.json").then(r => r.json()));
      
      eventsData = staticRes.products || [];
      storesData = staticRes.stores || [];
      console.log("✅ [Cloudflare Pages] 정적 행사 데이터 렌더링 완료:", eventsData.length, "개");
    } catch (e) {
      console.error("❌ 정적 JSON 데이터 로드 에러:", e);
    }
  }

  state.products = eventsData || [];
  state.stores = storesData || [];

  const statCount = document.getElementById("stat-total-items");
  if (statCount) statCount.textContent = state.products.length;

  applyFilters();
  renderStoreList();
}

// 3. 필터링 및 검색 이벤트
function initFilterEvents() {
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      state.searchQuery = e.target.value;
      applyFilters();
    });
  }

  document.getElementById("search-clear-btn")?.addEventListener("click", () => {
    if (searchInput) searchInput.value = "";
    state.searchQuery = "";
    applyFilters();
  });

  const brandBtns = document.querySelectorAll("#brand-selector .badge-btn");
  brandBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      brandBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.selectedBrand = btn.dataset.value;
      applyFilters();
    });
  });

  const eventBtns = document.querySelectorAll("#event-type-selector .badge-btn");
  eventBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      eventBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.selectedEventType = btn.dataset.value;
      applyFilters();
    });
  });

  document.getElementById("category-select")?.addEventListener("change", (e) => {
    state.selectedCategory = e.target.value;
    applyFilters();
  });

  document.getElementById("sort-select")?.addEventListener("change", (e) => {
    state.sortBy = e.target.value;
    applyFilters();
  });

  const mapBrandPills = document.querySelectorAll("#map-brand-filter .brand-pill");
  mapBrandPills.forEach(pill => {
    pill.addEventListener("click", () => {
      mapBrandPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      state.selectedMapBrand = pill.dataset.brand;

      if (state.mapEngine === "kakao") renderKakaoMapMarkers();
      else renderLeafletMapMarkers();

      renderStoreList();
    });
  });
}

// 4. 필터 로직
function applyFilters() {
  let list = [...state.products];

  if (state.selectedBrand !== "ALL") {
    list = list.filter(p => p.brand.toUpperCase() === state.selectedBrand.toUpperCase());
  }
  if (state.selectedEventType !== "ALL") {
    list = list.filter(p => p.event_type === state.selectedEventType);
  }
  if (state.selectedCategory !== "ALL") {
    list = list.filter(p => p.category === state.selectedCategory);
  }
  if (state.searchQuery.trim() !== "") {
    const q = state.searchQuery.trim().toLowerCase();
    list = list.filter(p => p.name.toLowerCase().includes(q));
  }

  if (state.sortBy === "unit_price_asc") {
    list.sort((a, b) => a.unit_price - b.unit_price);
  } else if (state.sortBy === "discount_desc") {
    list.sort((a, b) => b.discount_rate - a.discount_rate);
  } else if (state.sortBy === "price_asc") {
    list.sort((a, b) => a.price - b.price);
  } else if (state.sortBy === "price_desc") {
    list.sort((a, b) => b.price - a.price);
  }

  state.filteredProducts = list;
  renderProductGrid();
}

// 5. 상품 카드 그리드 렌더링
function renderProductGrid() {
  const container = document.getElementById("products-grid");
  const countText = document.getElementById("products-count-text");

  if (countText) {
    countText.innerHTML = `검색 결과 <span class="accent-text">${state.filteredProducts.length}</span>개`;
  }

  if (state.filteredProducts.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 4rem 1rem; color: var(--text-secondary);">
        <i class="fa-solid fa-ghost" style="font-size: 3rem; margin-bottom: 1rem;"></i>
        <p>조건에 맞는 행사 상품이 없습니다.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = state.filteredProducts.map(p => {
    const eventClass = p.event_type === "1+1" ? "event-1plus1" : "event-2plus1";
    return `
      <div class="product-card" onclick="openProductStoreOnMap('${p.name}', '${p.brand}')">
        <div class="product-badge-wrap">
          <span class="tag-brand ${p.brand}">${p.brand}</span>
          <span class="tag-event ${eventClass}">${p.event_type}</span>
        </div>
        <div class="product-img-wrap">
          <img src="${p.image}" alt="${p.name}" loading="lazy" referrerpolicy="no-referrer" onerror="this.src='https://images.unsplash.com/photo-1542838132-92c53300491e?w=300'" />
        </div>
        <div class="product-info">
          <span class="product-category">${p.category}</span>
          <h4 class="product-title">${p.name}</h4>
          <div class="price-box">
            <span class="original-price">정가 ${p.price.toLocaleString()}원</span>
            <div class="unit-price-wrap">
              <span class="unit-price">개당 ${Math.round(p.unit_price).toLocaleString()}원</span>
              <span class="unit-label">${p.discount_rate}% 혜택</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// 6. 이중 자동 보장 지도 엔진 (Kakao Map ➔ Leaflet Auto Fallback)
function initSmartMapEngine() {
  const container = document.getElementById("leaflet-map");
  if (!container) return;

  // 카카오 지도 SDK 시도
  if (typeof kakao !== "undefined" && kakao.maps) {
    kakao.maps.load(() => {
      try {
        const options = {
          center: new kakao.maps.LatLng(37.4979, 127.0276),
          level: 4
        };
        state.map = new kakao.maps.Map(container, options);
        state.mapEngine = "kakao";

        const zoomControl = new kakao.maps.ZoomControl();
        state.map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);

        document.getElementById("btn-recenter")?.addEventListener("click", () => {
          state.map.setCenter(new kakao.maps.LatLng(37.4979, 127.0276));
          state.map.setLevel(4);
        });

        document.getElementById("btn-busan")?.addEventListener("click", () => {
          state.map.setCenter(new kakao.maps.LatLng(35.1601, 129.1608));
          state.map.setLevel(4);
        });

        renderKakaoMapMarkers();
        console.log("✅ [Map Engine] 카카오 지도가 성공적으로 초기화되었습니다.");
      } catch (err) {
        console.warn("⚠️ 카카오 지도 도메인 인증 대기중, Leaflet 다크 지도로 자동 전환:", err);
        initLeafletFallbackMap(container);
      }
    });
  } else {
    initLeafletFallbackMap(container);
  }
}

// Leaflet 다크 지도 폴백 엔진 (도메인 미인증 시에도 100% 지도가 렌더링되도록 보장)
function initLeafletFallbackMap(container) {
  if (typeof L === "undefined") {
    const script = document.createElement("script");
    script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    const css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
    document.head.appendChild(css);
    document.head.appendChild(script);

    script.onload = () => buildLeafletMap(container);
  } else {
    buildLeafletMap(container);
  }
}

function buildLeafletMap(container) {
  state.mapEngine = "leaflet";
  state.map = L.map(container).setView([37.4979, 127.0276], 14);

  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap & CARTO',
    maxZoom: 19
  }).addTo(state.map);

  document.getElementById("btn-recenter")?.addEventListener("click", () => {
    state.map.setView([37.4979, 127.0276], 14);
  });

  document.getElementById("btn-busan")?.addEventListener("click", () => {
    state.map.setView([35.1601, 129.1608], 14);
  });

  renderLeafletMapMarkers();
}

// 7. 카카오 지도 마커 렌더링
function renderKakaoMapMarkers() {
  if (!state.map || typeof kakao === "undefined") return;

  if (state.markers) {
    state.markers.forEach(m => { if (m.setMap) m.setMap(null); });
  }
  state.markers = [];

  const brandColors = {
    "GS25": "#0072CE",
    "CU": "#652D90",
    "7-ELEVEN": "#00805A",
    "EMART24": "#FFB81C"
  };

  const storesToRender = state.selectedMapBrand === "ALL" 
    ? state.stores 
    : state.stores.filter(s => s.brand.toUpperCase() === state.selectedMapBrand.toUpperCase());

  const bounds = new kakao.maps.LatLngBounds();

  storesToRender.forEach(store => {
    const position = new kakao.maps.LatLng(store.lat, store.lng);
    bounds.extend(position);

    const color = brandColors[store.brand] || "#38bdf8";
    const appInfo = OFFICIAL_APP_LINKS[store.brand] || OFFICIAL_APP_LINKS["GS25"];

    const content = document.createElement("div");
    content.className = "kakao-custom-marker";
    content.style.cssText = `
      background: ${color};
      color: ${store.brand === 'EMART24' ? '#000' : '#fff'};
      font-weight: 900;
      font-size: 11px;
      padding: 6px 10px;
      border-radius: 14px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.5);
      border: 2px solid #fff;
      cursor: pointer;
      white-space: nowrap;
    `;
    content.innerHTML = `${store.name}`;

    const customOverlay = new kakao.maps.CustomOverlay({
      position: position,
      content: content,
      yAnchor: 1.3
    });

    customOverlay.setMap(state.map);
    state.markers.push(customOverlay);

    const popupContent = `
      <div style="padding:10px; min-width:240px; font-family:sans-serif; color:#0f172a;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <strong style="font-size:14px;">${store.name}</strong>
          <span style="background:#10b981; color:#fff; font-size:10px; font-weight:bold; padding:2px 6px; border-radius:4px;">행사 지정점</span>
        </div>
        <p style="font-size:11px; color:#64748b; margin-bottom:8px;">${store.address}</p>
        <button onclick="openStoreModal('${store.id}')" style="background:#0f172a; color:#fff; border:none; padding:6px 10px; border-radius:6px; font-size:11px; font-weight:bold; cursor:pointer; width:100%; margin-bottom:6px;">
          <i class="fa-solid fa-store"></i> 취급 행사 상품 확인
        </button>
        <a href="${appInfo.url}" target="_blank" style="display:block; text-align:center; background:${appInfo.bg}; color:${store.brand === 'EMART24' ? '#000' : '#fff'}; text-decoration:none; padding:6px 10px; border-radius:6px; font-size:11px; font-weight:bold;">
          <i class="fa-solid fa-mobile-screen"></i> ${store.brand} 앱에서 재고 확인 ➔
        </a>
      </div>
    `;

    const infowindow = new kakao.maps.InfoWindow({
      content: popupContent,
      removable: true
    });

    content.addEventListener("click", () => {
      if (state.activeInfowindow) state.activeInfowindow.close();
      infowindow.open(state.map, customOverlay);
      state.activeInfowindow = infowindow;
    });
  });

  if (storesToRender.length > 0) {
    state.map.setBounds(bounds);
  }
}

// Leaflet 마커 렌더링 (보장 폴백)
function renderLeafletMapMarkers() {
  if (!state.map || typeof L === "undefined") return;

  state.markers.forEach(m => state.map.removeLayer(m));
  state.markers = [];

  const brandColors = {
    "GS25": "#0072CE",
    "CU": "#652D90",
    "7-ELEVEN": "#00805A",
    "EMART24": "#FFB81C"
  };

  const storesToRender = state.selectedMapBrand === "ALL" 
    ? state.stores 
    : state.stores.filter(s => s.brand.toUpperCase() === state.selectedMapBrand.toUpperCase());

  storesToRender.forEach(store => {
    const color = brandColors[store.brand] || "#38bdf8";
    const appInfo = OFFICIAL_APP_LINKS[store.brand] || OFFICIAL_APP_LINKS["GS25"];

    const customIcon = L.divIcon({
      className: 'custom-map-pin',
      html: `
        <div style="
          background: ${color};
          color: ${store.brand === 'EMART24' ? '#000' : '#fff'};
          font-weight: 900;
          font-size: 11px;
          padding: 5px 8px;
          border-radius: 12px;
          box-shadow: 0 4px 14px rgba(0,0,0,0.5);
          border: 2px solid #fff;
          white-space: nowrap;
        ">
          ${store.name}
        </div>
      `,
      iconSize: [120, 30],
      iconAnchor: [60, 15]
    });

    const marker = L.marker([store.lat, store.lng], { icon: customIcon }).addTo(state.map);

    const popupContent = `
      <div style="color: #0f172a; font-family: sans-serif; padding: 4px; min-width: 220px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
          <strong style="font-size: 14px; color:#0f172a;">${store.name}</strong>
          <span style="background:#10b981; color:#fff; font-size:10px; font-weight:bold; padding:2px 6px; border-radius:4px;">행사 지정점</span>
        </div>
        <p style="font-size: 11px; color: #64748b; margin-bottom: 8px;">${store.address}</p>
        <button onclick="openStoreModal('${store.id}')" style="
          background: #0f172a;
          color: #fff;
          border: none;
          padding: 6px 10px;
          border-radius: 6px;
          font-size: 11px;
          font-weight: bold;
          cursor: pointer;
          width: 100%;
          margin-bottom: 5px;
        ">
          <i class="fa-solid fa-store"></i> 취급 행사 상품 확인
        </button>
        <a href="${appInfo.url}" target="_blank" style="
          display: block;
          text-align: center;
          background: ${appInfo.bg};
          color: ${store.brand === 'EMART24' ? '#000' : '#fff'};
          text-decoration: none;
          padding: 6px 10px;
          border-radius: 6px;
          font-size: 11px;
          font-weight: bold;
        ">
          <i class="fa-solid fa-mobile-screen"></i> ${store.brand} 앱에서 재고 확인 ➔
        </a>
      </div>
    `;

    marker.bindPopup(popupContent);
    state.markers.push(marker);
  });

  if (state.markers.length > 0) {
    const group = L.featureGroup(state.markers);
    state.map.fitBounds(group.getBounds().pad(0.1));
  }
}

// 8. 사이드바 매장 목록 렌더링
function renderStoreList() {
  const container = document.getElementById("store-list");
  if (!container) return;

  const storesToRender = state.selectedMapBrand === "ALL" 
    ? state.stores 
    : state.stores.filter(s => s.brand.toUpperCase() === state.selectedMapBrand.toUpperCase());

  container.innerHTML = storesToRender.map(s => `
    <div class="store-item" onclick="selectStoreOnMap('${s.id}', ${s.lat}, ${s.lng})">
      <div class="store-item-header">
        <span class="store-name">${s.name}</span>
        <span class="tag-brand ${s.brand}">${s.brand}</span>
      </div>
      <p class="store-address">${s.address}</p>
      <div class="store-inventory-summary">
        <span>지정 상태: <strong class="stock-count">1+1/2+1 공식 매장</strong></span>
      </div>
    </div>
  `).join("");
}

window.selectStoreOnMap = function(storeId, lat, lng) {
  if (state.mapEngine === "kakao" && state.map && typeof kakao !== "undefined") {
    const moveLatLon = new kakao.maps.LatLng(lat, lng);
    state.map.setCenter(moveLatLon);
    state.map.setLevel(3);
  } else if (state.mapEngine === "leaflet" && state.map) {
    state.map.setView([lat, lng], 16);
  }
};

window.openProductStoreOnMap = function(productName, brand) {
  document.querySelector('[data-tab="tab-map"]').click();
  state.selectedMapBrand = brand;

  const mapBrandPills = document.querySelectorAll("#map-brand-filter .brand-pill");
  mapBrandPills.forEach(p => {
    if (p.dataset.brand.toUpperCase() === brand.toUpperCase()) {
      p.classList.add("active");
    } else {
      p.classList.remove("active");
    }
  });

  if (state.mapEngine === "kakao") renderKakaoMapMarkers();
  else renderLeafletMapMarkers();

  renderStoreList();
};

// 9. 매장 상세 모달
window.openStoreModal = function(storeId) {
  const store = state.stores.find(s => s.id === storeId);
  if (!store) return;

  const appInfo = OFFICIAL_APP_LINKS[store.brand] || OFFICIAL_APP_LINKS["GS25"];

  document.getElementById("modal-store-brand").textContent = store.brand;
  document.getElementById("modal-store-brand").className = `brand-tag tag-brand ${store.brand}`;
  document.getElementById("modal-store-name").textContent = store.name;
  document.getElementById("modal-store-address").textContent = store.address;
  document.getElementById("modal-store-status").textContent = `${store.open24 ? '24시간 운영' : '일반 운영'} | 1+1 & 2+1 공식 수집 매장`;

  const invList = document.getElementById("modal-inventory-list");

  const deepLinkHtml = `
    <div style="grid-column: 1/-1; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 10px; padding: 1rem; margin-bottom: 1rem; text-align: center;">
      <p style="font-size: 0.82rem; color: #94a3b8; margin-bottom: 0.6rem;">💡 본 매장의 1초 단위 실시간 재고는 ${store.brand} 공식 스마트폰 앱에서 즉시 조회하실 수 있습니다.</p>
      <a href="${appInfo.url}" target="_blank" style="display: inline-block; background: ${appInfo.bg}; color: ${store.brand === 'EMART24' ? '#000' : '#fff'}; font-weight: 800; font-size: 0.85rem; padding: 0.6rem 1.4rem; border-radius: 8px; text-decoration: none;">
        <i class="fa-solid fa-mobile-screen"></i> ${appInfo.name} ➔
      </a>
    </div>
  `;

  if (store.inventory && store.inventory.length > 0) {
    invList.innerHTML = deepLinkHtml + store.inventory.map(item => `
      <div class="inventory-card">
        <div>
          <div class="item-name">${item.product_name}</div>
          <span class="item-event-tag">${item.event_type}</span>
        </div>
        <div>
          <span class="item-stock-badge in-stock">
            행사 취급중
          </span>
        </div>
      </div>
    `).join("");
  } else {
    invList.innerHTML = deepLinkHtml + `<p style="grid-column:1/-1; text-align:center; color:var(--text-muted);">등록된 행사 상품이 없습니다.</p>`;
  }

  document.getElementById("store-modal").classList.add("active");
};

function closeModal() {
  document.getElementById("store-modal").classList.remove("active");
}
