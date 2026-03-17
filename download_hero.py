from bing_image_downloader import downloader
import os
import shutil

query = "medical textiles manufacturing high quality hd"
name = "hero_bg"

downloader.download(query, limit=1,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60)

folder_path = os.path.join("dataset", query)
if os.path.exists(folder_path):
    files = os.listdir(folder_path)
    if files:
        img_file = files[0]
        ext = os.path.splitext(img_file)[1]
        src = os.path.join(folder_path, img_file)
        os.makedirs("static/images", exist_ok=True)
        dst = f"static/images/{name}{ext}"
        shutil.copy(src, dst)
        print(f"Downloaded and moved: {dst}")
