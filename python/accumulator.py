# -*- coding: utf-8 -*-

"""
http://www.paulgraham.com/accgen.html
http://www.knesl.com/articles/view/grahamuv-problem

Vytvoř akumulátorovou funkci, které předáš parametr a ona vrátí funkci
očekávající další parametr. Po předání parametru ti vrátí součet a změní
svůj stav tak, že příští zavolání bude sčítat předchozí hodnotu s dalším
parametrem.

V imaginárním jazyce bude použití:

>>> acc = create_accumulator(5)
>>> acc(1) # 6
>>> acc(1) # 7
>>> acc(3) # 10
"""

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals


class Accumulator:
    "Classic"
    def __init__(self, n):
        self._accumulator = n

    def __call__(self, i):
        self._accumulator += i
        return self._accumulator


def create_accumulator(n):
    while True:
        n += yield n


def callable_generator(function):
    def decorator(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)  # start up the generator

        return lambda v=None: generator.send(v)

    return decorator


@callable_generator
def decorated_create_accumulator(n):
    while True:
        n += yield n


if __name__ == "__main__":
    for fn in (Accumulator, decorated_create_accumulator):
        acc = fn(5)

        assert acc(1) == 6
        assert acc(1) == 7
        assert acc(3) == 10

    acc = create_accumulator(5)
    next(acc)
    assert acc.send(1) == 6
    assert acc.send(1) == 7
    assert acc.send(3) == 10
