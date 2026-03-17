import urllib.request
import re
import os

os.makedirs('static/images', exist_ok=True)

queries = [
    ("medical bandage roll isolated", "product_1"),
    ("surgical cotton roll isolated", "product_2"),
    ("gauze bandage roll", "product_3"),
    ("absorbent gauze roll medical", "product_4"),
    ("sterile cotton swabs medical", "product_5"),
    ("surgical face mask 3 ply", "product_6"),
    ("medical uniform doctor", "hero")
]

req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for q, name in queries:
    query = q.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    req = urllib.request.Request(url, headers=req_headers)
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        # Find image urls returning from google search (typically formatted in script tags, or img src)
        # Google uses some base64 or raw URLs. We can extract basic jpg URLs.
        urls = re.findall(r'(https?://[^"\']+\.jpg)', html)
        if urls:
            src_url = urls[0]
            print(f"Downloading {name} from {src_url}")
            urllib.request.urlretrieve(src_url, f"static/images/{name}.jpg")
        else:
            print(f"No JPG found for {name}")
    except Exception as e:
        print(f"Error for {name}: {e}")
