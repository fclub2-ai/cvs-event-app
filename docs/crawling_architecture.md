# 4대 편의점(GS25, CU, 세븐일레븐, 이마트24) 크롤링 & 데이터 연동 기술 분석 보고서

## 1. 개요 및 배경

본 보고서는 국내 주요 편의점 4사(GS25, 포켓CU, 세븐일레븐, 이마트24)의 **1+1 / 2+1 행사 상품 데이터 수집 파이프라인** 및 **실시간 재고 조회 한계와 기술적 대안**을 구체적으로 분석하고 설계 가이드를 제공합니다.

---

## 2. 편의점 4사 웹사이트/앱 크롤링 구조 분석

### ① GS25 (우리동네GS)
- **행사 페이지 URL**: `http://gs25.gsretail.com/gscvs/ko/products/youus-event`
- **수집 방식**:
  - Web Scraping: BeautifulSoup + Playwright/Selenium (동적 탭 및 AJAX 요청 처리)
  - API 엔드포인트 파싱: `/gscvs/ko/products/youus-event-search` (Form Data 기반 POST 요청)
- **유의 사항**: CSRF 토큰 및 Session Cookie 검증 필요.

### ② CU (포켓CU)
- **행사 페이지 URL**: `https://cu.bgfretail.com/event/plus.do`
- **수집 방식**:
  - HTML Form POST 크롤링: `pageIndex`, `listType` 파라미터 전송을 통해 1+1, 2+1 행사 상품 리스트 JSON/HTML 파싱.
  - 모바일 앱 백엔드 API: 네트워크 패킷 분석으로 앱 내 1+1 행사 탭 API 응답 수집 가능.

### ③ 세븐일레븐 (7-Eleven)
- **행사 페이지 URL**: `https://www.7-eleven.co.kr/product/presentList.asp`
- **수집 방식**:
  - Classic ASP 기반 파라미터 요청 (`pTab=1` : 1+1, `pTab=2` : 2+1).
  - BeautifulSoup4 기반의 파이프라인으로 간단하게 파싱 가능.

### ④ 이마트24 (emart24)
- **행사 페이지 URL**: `https://www.emart24.co.kr/product/eventProduct.asp`
- **수집 방식**:
  - React/Vue 기반 SPA 구조.
  - Playwright 또는 Puppeteer를 사용하여 렌더링 후 DOM 파싱 또는 XHR/Fetch API 모니터링 수집.

---

## 3. 크롤링 파이프라인 구축 시 기술적 리스크 및 해결책

| 이슈 항목 | 리스크 설명 | 권장 기술적 대안 (Best Practice) |
| :--- | :--- | :--- |
| **이미지 핫링크 (Hotlinking) 차단** | 본사 CDN에서 Referer 검증으로 이미지 엑박 현상 발생 | 수집 시 이미지 바이너리를 내 서버/S3에 저장하거나 썸네일 캐싱 서버 구축 |
| **WAF / IP 차단** | 짧은 시간 연속 요청 시 Web Application Firewall 차단 | `User-Agent` 순환, 요청 간 `0.5s~1s` 딜레이, 세션 재사용 |
| **월초 데이터 레이턴시** | 매월 1일 자정~오전 9시 사이 행사 데이터 일괄 교체 | 매월 1일 새벽 1시, 3시, 6시 Cron Job 스케줄러 재시도 로직 구성 |

---

## 4. 실시간 재고(Inventory) 데이터 연동의 기술적 한계 및 B2B 대안

### 1) 왜 전국 실시간 재고 크롤링은 불가능한가?
- **POS 매장 결제 동기화**: 실시간 재고는 매장 결제시 POS → 본사 DB로 차감되는 민감 트래픽임.
- **강력한 OAuth & 모바일 장비 식별자**: 앱 API 요청 시 디바이스 토큰 및 캡차(CAPTCHA), WAF 보호 적용.
- **IP 차단 및 영업방해 이슈**: 무단 크롤링 시 본사 보안팀의 법적 제재 및 IP 즉시 블랙리스트 등록.

### 2) 현실적인 B2B 연동 아키텍처
- 배달의민족, 요기요, 네이버 주문처럼 본사와 공식 **B2B API 제휴** 체결.
- Webhook 또는 주기적 Delta Sync 방식으로 매장별 SKU 재고 수량을 수신.

---

## 5. 결론 및 추천 아키텍처

- **마케팅 홍보 데이터(1+1, 2+1 행사 정보)**: 매월 1일 파이썬 자동화 크롤러(Cron)로 수집하여 서비스 DB 갱신.
- **실시간 재고(Inventory)**: 사용자 중심 UI에는 지도 API + 가상 POS 모의 재고(Mock POS Inventory Engine)를 바인딩하여 인터랙티브한 사용자 경험 제공.
