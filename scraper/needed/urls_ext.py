import os
import re

import requests


def extract_urls(error_text):
    # Pattern to match URLs after "Error downloading "
    pattern = r'Error downloading (https?://[^\s:]+)'
    
    # Find all matches
    urls = re.findall(pattern, error_text)

    return set(urls)

# Example usage:
with open('url_files.txt', 'r') as f:
    text = f.read()
    for url in text.splitlines():
        response = requests.get(url, stream=True)

        filename = f'./downloads/{url.split("/")[-1].split('?t=')[0].replace(' ', '_'
                        ).replace('\n', ''
                        ).replace('?', ''
                        ).replace('%20', ' '
                        ).replace('/', '_'
                        ).replace(':', '_'
                        ).replace('#', '')}'

        if os.path.exists(filename):
            continue

        print(f"downloading {url}")

        with open(filename, 'wb') as out:
            for chunk in response.iter_content(chunk_size=8192):
                out.write(chunk)
