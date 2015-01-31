# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals


class Class1(object):
    __slots__ = ("a", "b", "c")


class Class2(object):
    __slots__ = ()

    def __init__(self):
        self._a = ["a", "b", "c"]


class Slotless(object):
    pass


class Derived(Slotless):
    __slots__ = ()

    def __init__(self):
        self._a = ["a", "b", "c"]


if __name__ == "__main__":
    o1 = Class1()
    o1.a, o1.b, o1.c = 1, 1, 1

    try:
        o1._d = 1
        raise ValueError("Attribute '_d' should raise exception")
    except AttributeError:
        pass

    try:
        o2 = Class2()
        raise ValueError("Attribute '_a' should raise exception")
    except AttributeError:
        pass

    try:
        o3 = Derived()
    except AttributeError:
        raise ValueError("Attribute '_a' shouldn't raise exception")
