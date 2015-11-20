# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import requests
import grequests

from datetime import datetime


if __name__ == "__main__":
    urls = [
        'http://www.heroku.com',
        'http://python-tablib.org',
        'http://httpbin.org',
        'http://python-requests.org',
        'http://kennethreitz.com',
        'http://google.com',
        'http://google.sk',
        'http://google.cz',
        'http://www.timeapi.org/utc/now',
    ]

    rs = (grequests.get(u) for u in urls)

    session = requests.Session()
    timer_start = datetime.now()
    for url in urls:
        response = session.get(url)
        print(response.request, "->", response)
        delta = round((datetime.now() - timer_start).total_seconds(), 3)
        print("timer", delta)

    timer_start = datetime.now()
    for response in grequests.imap(rs, size=20):
        print(response.request, "->", response)
        delta = round((datetime.now() - timer_start).total_seconds(), 3)
        print("ASYNC timer", delta)
