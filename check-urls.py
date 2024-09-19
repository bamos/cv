#!/usr/bin/env python3

import re
import requests
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

def extract_urls(file_path):
    url_pattern = r'(https?://[^\s\'\}]+)'
    with open(file_path, 'r') as file:
        content = file.read()
    urls = re.findall(url_pattern, content)
    urls = list(set(urls))
    return urls

def print_url_status(url):
    if 'scholar' in url or 'linkedin' in url:
        # ignore Google Scholar and LinkedIn
        return
    try:
        response = requests.head(url, headers=headers, timeout=5)
        if response.status_code in [200, 302]:
            return
        elif response.status_code == 301: # redirect
            redirected_url = response.headers.get('Location')
            print(f'{response.status_code}: {url} -> {redirected_url}')
        else:
            print(f'{response.status_code}: {url}')
    except requests.RequestException as e:
        print(f"Invalid (Error: {e})")
        pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    urls = extract_urls(file_path)

    if not urls:
        print("No URLs found in the file.")
        sys.exit(0)

    print(f"Found {len(urls)} URL(s). Checking status...\n")

    with Pool(processes=32) as pool:
        pool.map(print_url_status, urls)

if __name__ == "__main__":
    main()
