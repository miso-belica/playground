# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys


def unicode_compatible(cls):
    if sys.version_info[0] >= 3:
        cls.__bytes__ = lambda self: self.__str__().encode("utf-8")
        cls.__str__ = cls.__unicode__
    else:
        cls.__str__ = lambda self: self.__unicode__().encode("utf-8")

    return cls


@unicode_compatible
class Object1(object):
    def __init__(self, arg):
        self._arg = arg

    def __unicode__(self):
        return "€€€€€€€€€€€€€€€€€€€"


@unicode_compatible
class Object2(Object1):

    def __unicode__(self):
        return "ľščťžýáíéäúôň"


if __name__ == "__main__":
    o = Object2(29)

    if sys.version_info[0] >= 3:
        assert "ľščťžýáíéäúôň".encode("utf-8") == bytes(o)
        assert "ľščťžýáíéäúôň" == str(o)

        assert "ľščťžýáíéäúôň".encode("utf-8") != str(o)
        assert "ľščťžýáíéäúôň" != bytes(o)
    else:
        assert "ľščťžýáíéäúôň".encode("utf-8") == str(o)
        assert "ľščťžýáíéäúôň" == unicode(o)

        # these emit warnings
        assert "ľščťžýáíéäúôň".encode("utf-8") != unicode(o)
        assert "ľščťžýáíéäúôň" != str(o)
