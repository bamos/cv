#!/usr/bin/env python3

import re
import requests
from requests import exceptions as requests_exc
import sys
from multiprocessing import Pool
from urllib3 import exceptions as urllib3_exc

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

IGNORED_REQUEST_EXCEPTIONS = (
    requests_exc.ConnectTimeout,
    requests_exc.ReadTimeout,
)

IGNORED_CAUSE_EXCEPTIONS = (
    urllib3_exc.MaxRetryError,
    urllib3_exc.ConnectTimeoutError,
)

def should_ignore_error(err):
    if isinstance(err, IGNORED_REQUEST_EXCEPTIONS):
        return True
    cause = err.__cause__
    while cause:
        if isinstance(cause, IGNORED_CAUSE_EXCEPTIONS):
            return True
        cause = cause.__cause__
    return False

def extract_urls(file_path):
    url_pattern = r'(https?://[^\s\'\"\}\)\<\>]+)'
    with open(file_path, 'r') as file:
        content = file.read()
    urls = re.findall(url_pattern, content)
    urls = list(set(urls))
    return urls

def check_url(url):
    if 'scholar' in url or 'linkedin' in url:
        # ignore Google Scholar and LinkedIn
        return None
    try:
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        if response.status_code in [200, 301, 302, 403, 429]:
            return None
        if response.status_code == 405:
            raise requests.RequestException("HEAD not allowed")
        return f'{response.status_code}: {url}'
    except requests.RequestException as e:
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            if response.status_code in [200, 301, 302, 403, 429]:
                return None
            return f'{response.status_code}: {url}'
        except requests.RequestException as get_error:
            if should_ignore_error(get_error):
                print(f'\n--- Skipping error for {url}\n{get_error}')
                return None
            return f'Invalid (Error: {get_error}) {url}'

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
        results = pool.map(check_url, urls)

    failures = [result for result in results if result]

    if len(failures) > 0:
        for failure in failures:
            print(failure)
        sys.exit(1)

    print("All URLs are valid.")

if __name__ == "__main__":
    main()
