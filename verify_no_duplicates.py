import re

INDEX_PATH = r"C:\Users\fclub\cvs-event-app\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

script_count = len(re.findall(r'<script', html, re.IGNORECASE))
print(f"Total <script> tags: {script_count}")

# Check lines at the end of the file
lines = html.splitlines()
print(f"Total lines: {len(lines)}")
print("Last 15 lines of index.html:")
for l in lines[-15:]:
    print(l)
