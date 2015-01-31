# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals


def finally_beats_return():
    try:
        return 84
    finally:
        return 48


if __name__ == "__main__":
    assert 48 == finally_beats_return()
