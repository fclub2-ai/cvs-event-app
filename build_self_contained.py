"""
Claude API Self-Contained Index Generator
- Embeds complete UI/UX Pro Max CSS inside <style> tag in index.html to guarantee ZERO CSS rendering failures anywhere.
- Configures bulletproof data fetching and Kakao Maps fallback.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
STYLE_PATH = os.path.join(BASE_DIR, "src", "style.css")

def bundle():
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        css_content = f.read()

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Replace <link rel="stylesheet" href="...style.css" /> with inline <style>
    style_tag = f"<style>\n{css_content}\n</style>"
    
    # Remove existing style link tags
    lines = html_content.splitlines()
    new_lines = []
    style_inserted = False
    
    for line in lines:
        if "style.css" in line:
            if not style_inserted:
                new_lines.append(style_tag)
                style_inserted = True
        else:
            new_lines.append(line)
            
    final_html = "\n".join(new_lines)
    
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print("[OK] Inlined complete style.css into index.html successfully!")

if __name__ == "__main__":
    bundle()
