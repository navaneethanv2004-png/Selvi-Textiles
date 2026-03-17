import os
import requests
from duckduckgo_search import DDGS

os.makedirs("static/images", exist_ok=True)

queries = [
    (1, "Medical Bandage white background hd"),
    (2, "Surgical Cotton Roll medical high resolution"),
    (3, "Medical Roller Bandage white background isolated"),
    (4, "Medical Gauze Roll isolated"),
    (5, "Sterile medical cotton swabs isolated"),
    (6, "Surgical mask 3 ply isolated hd")
]

with DDGS() as ddgs:
    for product_id, query in queries:
        try:
            results = list(ddgs.images(query, max_results=5))
            for res in results:
                url = res['image']
                try:
                    r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                    r.raise_for_status()
                    ext = url.split('.')[-1].split('?')[0][:4]
                    if ext.lower() not in ['jpg', 'jpeg', 'png', 'webp']: 
                        ext = 'jpg'
                    filepath = f"static/images/product_{product_id}.jpg"
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                    print(f"Success: {filepath} from {url}")
                    break
                except Exception as e:
                    pass
        except Exception as e:
            print(f"DDGS error: {e}")
