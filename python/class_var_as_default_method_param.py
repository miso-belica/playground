# -*- coding: utf-8 -*-


class Example:
    _VARIABLE = 129

    def __init__(self):
        self._error = 1

    def method(self, parameter: int = _VARIABLE):
        return parameter + self._error


def test_default_parameter_is_returned():
    o = Example()

    assert o.method() == 130


def test_given_parameter_is_returned():
    o = Example()

    assert o.method(36) == 37
