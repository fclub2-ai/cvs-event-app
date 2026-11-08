import zipfile
import os

zip_name = "cvs-finder-cloudflare.zip"
base_dir = r"C:\Users\fclub\cvs-event-app"
zip_path = os.path.join(base_dir, zip_name)

files_to_pack = [
    "index.html",
    "style.css",
    "_headers",
    "cvs_data.json"
]

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for filename in files_to_pack:
        file_full_path = os.path.join(base_dir, filename)
        if os.path.exists(file_full_path):
            zipf.write(file_full_path, arcname=filename)
            print(f"[PACKED] {filename} ({os.path.getsize(file_full_path)} bytes)")

    app_js_path = os.path.join(base_dir, "src", "app.js")
    if os.path.exists(app_js_path):
        zipf.write(app_js_path, arcname="src/app.js")
        print(f"[PACKED] src/app.js ({os.path.getsize(app_js_path)} bytes)")

print(f"\nCreated deployment ZIP package: {zip_path}")
print(f"Total ZIP size: {os.path.getsize(zip_path) / 1024:.1f} KB ({os.path.getsize(zip_path) / (1024*1024):.2f} MB)")
