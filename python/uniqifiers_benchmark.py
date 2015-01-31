# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import time

from random import shuffle
from collections import OrderedDict


def f1(seq):  # Raymond Hettinger
    # not order preserving
    set = {}
    map(set.__setitem__, seq, [])
    return set.keys()


def f2(seq):   # *********
    # order preserving
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked


def f3(seq):
    # Not order preserving
    keys = {}
    for e in seq:
        keys[e] = 1
    return keys.keys()


def f4(seq):  # ********** order preserving
    noDupes = []
    [noDupes.append(i) for i in seq if not noDupes.count(i)]
    return noDupes


def f5(seq, idfun=None):  # Alex Martelli ******* order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def f5b(seq, idfun=None):  # Alex Martelli ******* order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker not in seen:
            seen[marker] = 1
            result.append(item)

    return result


def f7(seq):
    # Not order preserving
    return list(set(seq))


def f12(seq):
    # Not order preserving
    return list(frozenset(seq))


def f8(seq):  # Dave Kirby
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]


def f9(seq):
    # Not order preserving
    return {}.fromkeys(seq).keys()


def f10(seq, idfun=None):  # Andrew Dalke
    # Order preserving
    return list(_f10(seq, idfun))


def _f10(seq, idfun=None):
    seen = set()
    if idfun is None:
        for x in seq:
            if x in seen:
                continue
            seen.add(x)
            yield x
    else:
        for x in seq:
            x = idfun(x)
            if x in seen:
                continue
            seen.add(x)
            yield x


def f11(seq):  # f10 but simpler
    # Order preserving
    return list(_f11(seq))


def _f11(seq):
    seen = set()
    for x in seq:
        if x not in seen:
            seen.add(x)
            yield x


def f13(seq):  # Michal Belica
    # Order preserving
    seen = set()
    data = []
    for i in seq:
        if i not in seen:
            data.append(i)
            seen.add(i)

    return data


def f14(seq):  # Michal Belica
    # Order preserving
    return list(OrderedDict.fromkeys(seq))
    # return list(OrderedDict.fromkeys(seq).keys())


def timing(f, n, a):
    r = range(n)
    expected = list(sorted(frozenset(a)))

    t1 = time.clock()
    for i in r:
        assert list(sorted(f(a))) == expected, (
            "%s: %r != %r" % (f.__name__, list(sorted(f(a))), expected)
        )
    t2 = time.clock()

    print(f.__name__, round(t2 - t1, 3))


def get_random_string(length=10, loweronly=1, numbersonly=0, lettersonly=0):
    """ return a very random string """
    _letters = 'abcdefghijklmnopqrstuvwxyz'
    if numbersonly:
        l = list('0123456789')
    elif lettersonly:
        l = list(_letters + _letters.upper())
    else:
        lowercase = _letters+'0123456789'*2
        l = list(lowercase + lowercase.upper())
    shuffle(l)
    s = ''.join(l)
    if len(s) < length:
        s = s + get_random_string(loweronly=1)
    s = s[:length]
    if loweronly:
        return s.lower()
    else:
        return s


testdata = {}
for i in range(35):
    k = get_random_string(5, lettersonly=1)
    v = get_random_string(100)
    testdata[k] = v


testdata = [int(x) for x in list('21354612')]
testdata += list('abcceeaa5efm')


class X:
    def __init__(self, n):
        self.foo = n

    def __repr__(self):
        return "<foo %r>" % self.foo

    def __cmp__(self, e):
        return cmp(self.foo, e.foo)


testdata = []
for i in range(10000):
    testdata.append(get_random_string(3, loweronly=True))
# testdata = ['f','g','c','d','b','a','a']


# order_preserving = f2, f4, f5, f5b, f8, f10, f11
order_preserving = f5, f5b, f8, f10, f11, f13, f14

not_order_preserving = f1, f3, f7, f9, f12
if sys.version_info[0] >= 3:
    # f1 is not working in py3k
    not_order_preserving = not_order_preserving[1:]
testfuncs = order_preserving + not_order_preserving


for f in testfuncs:
    if f in order_preserving:
        print("* ", end="")
    timing(f, 500, testdata)
