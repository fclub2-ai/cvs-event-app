import json
import os

def apply_urls():
    if not os.path.exists("harvested_48_results.json"):
        print("harvested_48_results.json does not exist yet!")
        return

    with open("harvested_48_results.json", "r", encoding="utf-8") as f:
        harvested = json.load(f)

    print(f"Loaded {len(harvested)} harvested ImgBB URLs.")

    # Update cvs_data.json
    for data_path in ["cvs_data.json", "backend/cvs_data.json"]:
        if not os.path.exists(data_path):
            continue
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        products = data.get("products", data) if isinstance(data, dict) else data

        updated_count = 0
        for p in products:
            name = p["name"]
            base_name = name.split(") ")[-1] if ") " in name else name
            if base_name in harvested:
                p["image"] = harvested[base_name]
                updated_count += 1

        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Updated {updated_count} product items in {data_path}")

    # Run build_full_bundle.py to update index.html
    import subprocess
    res = subprocess.run(["python", "build_full_bundle.py"], capture_output=True, text=True, encoding="utf-8")
    print("Bundle build result:", res.stdout or res.stderr)

if __name__ == "__main__":
    apply_urls()
