"""
CVS-FINDER 4대 편의점 공식 행사 데이터 & 배포 ZIP 원클릭 자동 갱신 스크립트
"""

import sys
import subprocess
import os

sys.stdout.reconfigure(encoding='utf-8')

PYTHON_EXE = sys.executable

def run_step(description, command):
    print("\n" + "=" * 80)
    print(f"🚀 [STEP] {description}")
    print("=" * 80)
    res = subprocess.run([PYTHON_EXE] + command, capture_output=True, text=True, encoding='utf-8')
    if res.returncode == 0:
        print(res.stdout)
        print(f"✅ {description} 완료!")
    else:
        print(f"❌ {description} 실패:")
        print(res.stderr)
        sys.exit(1)

def main():
    print("================================================================================")
    print("      CVS-FINDER 4대 편의점 공식 본사 데이터 100% 원클릭 자동 갱신 시작        ")
    print("================================================================================")

    # 1. 4대 편의점 공식 사이트 데이터 동기화
    run_step("CU / GS25 / 세븐일레븐 / 이마트24 공식 본사 데이터 실시간 수집", ["sync_official_cvs_data.py"])

    # 2. index.html 인라인 번들링
    run_step("index.html 인라인 코드 & 4,630+개 핫딜 데이터 결합 번들링", ["build_full_bundle.py"])

    # 3. Cloudflare Pages 배포용 ZIP 생성
    run_step("Cloudflare Pages 최신 배포 ZIP 패키지 생성 (cvs-finder-cloudflare.zip)", ["create_zip_package.py"])

    print("\n" + "=" * 80)
    print("🎉 [모든 작업 완료] Cloudflare Pages 배포 준비가 완료되었습니다!")
    print("📦 생성된 배포 ZIP 파일 위치: C:\\Users\\fclub\\cvs-event-app\\cvs-finder-cloudflare.zip")
    print("================================================================================")

if __name__ == "__main__":
    main()
