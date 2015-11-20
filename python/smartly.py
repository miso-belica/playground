# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import requests


def main():
    next_url = "/racetus"
    while next_url:
        response = requests.get(
            "https://fasttrack.herokuapp.com" + next_url,
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()

        next_url = response.json()["next"]
        print(next_url)


if __name__ == "__main__":
    main()
