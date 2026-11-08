import re
import os
import sys

INDEX_PATH = r"C:\Users\fclub\cvs-event-app\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Check for any unescaped </script> inside script tags
scripts = re.findall(r'<script.*?>(.*?)</script>', html, flags=re.DOTALL)
print(f"Total <script> tags found in index.html: {len(scripts)}")

for idx, s in enumerate(scripts):
    print(f"Script #{idx+1} length: {len(s)} chars")
    if "</script>" in s:
        print(f"ERROR: Found unescaped </script> inside Script #{idx+1}!")
    else:
        print(f"OK: Script #{idx+1} is clean!")

if "adsbygoogle" in html:
    print("OK: AdSense script & slots found in index.html!")
