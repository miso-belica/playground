# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from itertools import chain


class SmartIterator(object):
    """
    Iterator with ability to find out usefull information
    during iteration (first/last lement, has more elements, etc.).

    :copyright: 2013, Michal Belica
    :license: MIT
    """
    def __init__(self, iterable):
        self._iterable = iter(iterable)
        self._cycle = -1
        self._next = None
        self._next_cached = False

    def is_first(self):
        return self._cycle == 0

    def is_last(self):
        return not self.has_next()

    def has_next(self):
        if self._next_cached:
            return True

        try:
            self._next = next(self._iterable)
            self._next_cached = True
            return True
        except StopIteration:
            return False

    def is_odd(self):
        """
        Returns ``True`` if it's odd iteration (index is even number).
        Otherwise ``False`` is returned.
        """
        return not self.is_even()

    def is_even(self):
        """
        Returns ``True`` if it's even iteration (index is zero or odd number).
        Otherwise ``False`` is returned.
        """
        return bool(self._cycle & 1)

    def is_empty(self):
        if self._cycle != -1:
            return False
        else:
            return not self.has_next()

    def rewind(self):
        raise NotImplementedError("Iterator with cache is not implemented")

    def __len__(self):
        raise NotImplementedError("Iterator with cache is not implemented")

    def __int__(self):
        """Returns index of iteration (incremented from zero)."""
        return self._cycle

    def __iter__(self):
        return self

    def __next__(self):
        self._cycle += 1

        if self._next_cached:
            self._next_cached = False
            return self, self._next
        else:
            return self, next(self._iterable)

    next = __next__


def iterate(iterable):
    return SmartIterator(iterable)


if __name__ == "__main__":
    iterables = (
        (i for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)),
        chain((0,), (1, 2, 3), (4, 5, 6), (7, 8, 9)),
    )

    for iterable in iterables:
        index = 0

        for i, value in iterate(iterable):
            assert int(i) == index
            assert value == index
            assert (int(i) in (0, 2, 4, 6, 8) and i.is_odd()) or not i.is_odd()
            assert (int(i) in (1, 3, 5, 7, 9) and i.is_even()) or not i.is_even()
            assert (int(i) == 0 and i.is_first()) or not i.is_first()
            assert (int(i) == 9 and i.is_last()) or not i.is_last()
            assert (0 <= int(i) < 9 and i.has_next()) or not i.has_next()

            index += 1
