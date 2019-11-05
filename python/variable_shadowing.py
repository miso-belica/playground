# -*- coding: utf-8 -*-

from typing import Iterable


def test_shadow_given_parameter():
    assert _function(1, []) == 1
    assert _function(1, [2, 3, 4]) == 4


def _function(variable, iterable: Iterable):
    for variable in iterable:
        pass

    return variable
