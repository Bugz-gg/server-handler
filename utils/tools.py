import requests
from urllib.parse import urlparse
import os


def download_file(url, folder, base_name="file"):
    os.makedirs(folder, exist_ok=True)

    path = urlparse(url).path
    ext = os.path.splitext(path)[1]

    if not ext:
        ext = ""

    i = 1
    while True:
        filename = f"{base_name}{i}{ext}"
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            break
        i += 1

    response = requests.get(url)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath
