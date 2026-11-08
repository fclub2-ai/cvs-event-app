"""
Claude API Clean Self-Contained Bundle Generator
- Inlines CSS, JS, and EMBEDDED_CVS_DATA into index.html
- Completely self-contained for Cloudflare Pages with zero external asset dependency
"""

import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
APP_PATH = os.path.join(BASE_DIR, "src", "app.js")
CSS_PATH = os.path.join(BASE_DIR, "style.css")
DATA_PATH = os.path.join(BASE_DIR, "backend", "cvs_data.json")

def bundle():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    with open(APP_PATH, "r", encoding="utf-8") as f:
        js = f.read()

    with open(CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Strip any existing inline script tags or style tags that were previously injected
    html = re.sub(r'<script>\s*window\.EMBEDDED_CVS_DATA\s*=\s*\{.*?\};\s*</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)

    # 2. Inject single clean inlined <style>
    inline_css_tag = f'<style id="inlined-style">\n{css}\n</style>'
    if '<link rel="stylesheet" href="style.css">' in html:
        html = html.replace('<link rel="stylesheet" href="style.css">', inline_css_tag)
    else:
        html = html.replace('</head>', f'{inline_css_tag}\n</head>')

    # 3. Inject user's exact Google AdSense Script in <head>
    user_adsense_script = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4922796585485840" crossorigin="anonymous"></script>'
    if "pagead2.googlesyndication.com" not in html:
        html = html.replace("</head>", f"  {user_adsense_script}\n</head>")

    # 4. Top Banner AdSense Container (Using real slot ID 5682038219)
    top_ad_html = '''
      <!-- [AdSense] 상단 반응형 디스플레이 광고 배너 -->
      <div class="adsense-banner-wrapper glass-card" style="max-width:1360px; margin: 1rem auto; padding: 1rem; text-align: center; overflow: hidden; background: rgba(19, 27, 38, 0.75); border: 1px solid rgba(56, 189, 248, 0.25);">
        <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">ADVERTISEMENT</div>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-4922796585485840"
             data-ad-slot="5682038219"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
      </div>
'''
    if "adsense-banner-wrapper" not in html:
        html = html.replace('<div class="filter-panel glass-card">', f'{top_ad_html}\n      <div class="filter-panel glass-card">')

    total_prods = len(data.get("products", []))
    html = re.sub(r'<span class="stat-num" id="stat-total-items">\d+</span>', f'<span class="stat-num" id="stat-total-items">{total_prods}</span>', html)

    # 5. Create fresh embedded scripts
    js_safe = js.replace("</script>", "<\\/script>")
    embedded_data_script = f"<script>\nwindow.EMBEDDED_CVS_DATA = {json.dumps(data, ensure_ascii=False)};\n</script>"
    embedded_app_js = f"<script>\n{js_safe}\n</script>"

    lines = html.splitlines()
    new_lines = []
    
    for line in lines:
        if "dapi.kakao.com" in line:
            new_lines.append(line)
            new_lines.append(embedded_data_script)
            new_lines.append(embedded_app_js)
            break
        else:
            new_lines.append(line)

    new_lines.append("</body>")
    new_lines.append("</html>")
    
    final_html = "\n".join(new_lines)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"[SUCCESS] Inlined CSS & JS! Cleaned and bundled index.html ({len(final_html)/1024:.1f} KB)")

if __name__ == "__main__":
    bundle()
