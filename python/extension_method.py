# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals


def main():
    object = Clazz()

    ext(object)

    assert ("public", "_protected", "__private", "orig:default") == object.orig()
    assert ("public", "_protected", "__private", "orig:arg") == object.orig("orig:arg")
    assert ("public", "_protected", "__private", "orig:class") == Clazz.orig(object, "orig:class")

    assert ("public", "_protected", None, "ext:default") == object.ext()
    assert ("public", "_protected", None, "ext:arg") == object.ext("ext:arg")
    assert ("public", "_protected", None, "ext:class") == Clazz.ext(object, "ext:class")


def extension_method(cls):
    def decorate(f):
        setattr(cls, f.__name__, f)
        return f

    return decorate


class Clazz(object):
    def __init__(self):
        self.public = "public"
        self._protected = "_protected"
        self.__private = "__private"

    def orig(self, msg="orig:default"):
        return self.public, self._protected, self.__private, msg


@extension_method(Clazz)
def ext(self, msg="ext:default"):
    try:
        self.__private
        assert False, "Extension method should not see private attribute."
    except AttributeError:
        assert True

    return self.public, self._protected, None, msg


if __name__ == "__main__":
    main()
