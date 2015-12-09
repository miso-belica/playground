# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from datetime import datetime
from collections import defaultdict
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession


URLS = [
    "https://unknown.org/typo",
    "https://httpbin.org/redirect/20",
    "https://httpbin.org/delay/5",
    "https://httpbin.org/get",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/403",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/delay/2",
]


MAX_RETRIES = 3
RETRIES = defaultdict(int)  # URL: count_of_retries


if __name__ == "__main__":
    session = FuturesSession(max_workers=30)
    futures = {session.get(u): u for u in URLS}

    start = datetime.now()
    while futures:
        print("-" * 80)
        for response_future in as_completed(futures):
            url = futures[response_future]

            try:
                response = response_future.result()
            except:
                RETRIES[url] += 1
                continue

            delta = datetime.now() - start
            print("{} in {} sec. | {} {}".format(url, delta.total_seconds(), response.status_code, response.reason))

            if not response.ok:
                RETRIES[url] += 1

        futures = {session.get(u): u for u, c in RETRIES.items() if c < MAX_RETRIES}

    print("!" * 80)
    for url in (url for url, count in RETRIES.items() if count >= MAX_RETRIES):
        print("{} failed.".format(url))
