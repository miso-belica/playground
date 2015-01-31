# -*- coding: utf-8 -*-

"""
Thre is a package for this now.
See https://github.com/pydanny/cached-property
"""

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from functools import wraps


def cached_property(getter):
    """
    Decorator that converts a method into memoized property.
    The decorator works as expected only for classes with
    attribute '__dict__' and immutable properties.

    TODO: delete cache if setter for property is invoked

    :copyright: 2013, Michal Belica
    :license: MIT
    """
    @wraps(getter)
    def decorator(self):
        key = "_cached_property_" + getter.__name__

        if not hasattr(self, key):
            setattr(self, key, getter(self))

        return getattr(self, key)

    return property(decorator)


class MutableClass(object):
    def __init__(self, stuff, index=-1):
        self._stuff = stuff
        self._index = index

    @cached_property
    def sequence(self):
        "Docstring for sequence."
        self._index += 1
        return self._index

    @cached_property
    def stuff(self):
        return self._stuff

    @stuff.setter
    def stuff(self, stuff):
        self._stuff = stuff


if __name__ == "__main__":
    cls = MutableClass(22)

    assert MutableClass.sequence.fget.__name__ == "sequence"
    assert MutableClass.sequence.__doc__ == "Docstring for sequence."

    # method is invoked only once
    assert cls.sequence == 0, cls.sequence
    assert cls._index == 0, cls._index
    assert cls.sequence == 0, cls.sequence
    assert cls._index == 0, cls._index
    assert cls.sequence == 0, cls.sequence
    assert cls._index == 0, cls._index

    # you can change property that is not cached yet
    # this is not a feature (instances should be immutable)
    cls.stuff = 11
    assert cls.stuff == 11, cls.stuff

    # changes are useless if property is cached
    cls.stuff = 22
    assert cls.stuff == 11, cls.stuff
    assert cls._stuff == 22, cls._stuff

    class_ = MutableClass(122, index=99)

    # method is invoked only once
    assert class_.sequence == 100, class_.sequence
    assert class_._index == 100, class_._index
    assert class_.sequence == 100, class_.sequence
    assert class_._index == 100, class_._index
    assert class_.sequence == 100, class_.sequence
    assert class_._index == 100, class_._index

    # you can change property that is not cached yet
    # this is not a feature (instances should be immutable)
    class_.stuff = 111
    assert class_.stuff == 111, class_.stuff

    # changes are useless if property is cached
    class_.stuff = 122
    assert class_.stuff == 111, class_.stuff
    assert class_._stuff == 122, class_._stuff
