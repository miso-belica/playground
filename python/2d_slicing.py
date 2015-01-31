# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals


class Matrix(object):
    def __init__(self, *args):
        self._args = args

    def __getitem__(self, index):
        if not isinstance(index, tuple):
            raise TypeError("Index should by tuple, not " + type(index).__name__)

        row, col = index
        args = self._args[row]

        return tuple(map(lambda r: r[col], args))

if __name__ == "__main__":
    m = Matrix(
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    )

    print(m[0:, 0:-1])
