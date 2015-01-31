# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import math


class Vector(object):
    def __init__(self, *values):
        self._values = tuple(values)

    def __len__(self):
        """
        Computes length/norm/magnitude of vector.
        This is usually denoted by ||d||.
        """
        length = math.sqrt(sum(v**2 for v in self._values))
        return int(round(length))


if __name__ == "__main__":
    vector = Vector(1, 1, 1, 1)
    assert math.sqrt(4) - 0.001 <= len(vector) <= math.sqrt(4) + 0.001
