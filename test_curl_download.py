import subprocess
import os

url = "https://view01.wemep.co.kr/wmp-product/1/956/824969561/824969561.jpg"
output_file = "test_vita500.jpg"

cmd = [
    "curl.exe", "-s", "-L",
    "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "-o", output_file,
    url
]

res = subprocess.run(cmd)
if os.path.exists(output_file):
    size = os.path.getsize(output_file)
    print(f"Downloaded {output_file}: {size} bytes")
else:
    print("Failed to download")
