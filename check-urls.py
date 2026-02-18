#!/usr/bin/env python3

import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import sys
from multiprocessing import Pool

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

IGNORED_URLS = {
    'https://pcts.princeton.edu/events/2025/physics-john-hopfield', # 403
    'https://research.adobe.com', # SSLError
}

def extract_urls(file_path):
    url_pattern = r'(https?://[^\s\'\"\}\)\<\>]+)'
    with open(file_path, 'r') as file:
        content = file.read()
    urls = re.findall(url_pattern, content)
    urls = list(set(urls))
    return urls

def check_url(url):
    """Check a URL with retry logic."""
    if url in IGNORED_URLS or 'linkedin.com' in url:
        print(f'skipping: {url}')
        return None

    session = requests.Session()
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=1.0,
        status_forcelist=[408, 429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.head(url, headers=headers, timeout=10, allow_redirects=True)
        if response.status_code in [202, 405]:
            response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
        if response.status_code in [400, 403]:
            print(f'{response.status_code} (ignored): {url}')
            return None
        if response.status_code == 200:
            return None
        return f'{response.status_code}: {url}'
    except requests.RequestException as e:
        if type(e).__name__ == 'RetryError':
            print(f'{type(e).__name__} (ignored): {url}')
            return None
        return f'{type(e).__name__}: {url}'

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    urls = extract_urls(file_path)

    if not urls:
        print("No URLs found in the file.")
        sys.exit(0)

    print(f"Found {len(urls)} URL(s). Checking status...")

    with Pool(processes=32) as pool:
        results = pool.map(check_url, urls)

    failures = [result for result in results if result]

    if len(failures) > 0:
        for failure in failures:
            print(failure)
        sys.exit(1)

    print("\nURLs are valid.")

if __name__ == "__main__":
    main()
