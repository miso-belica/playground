# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import traceback


def bother():
    """Prints oroginal stack trace of exception."""
    raise Exception("Take your hands out of me!")


def variable_definition_inside_try_block():
    """Is variable initialized outside the try/except block?"""
    try:
        var = 'try block'
    except:
        var = 'except block'
    finally:
        assert "try block" == var

    assert "try block" == var

    try:
        raise Exception("Hurts, huh?")
    except:
        variable = 'except block'
    finally:
        assert "except block" == variable

    assert "except block" == variable


if __name__ == "__main__":
    variable_definition_inside_try_block()

    try:
        bother()
    except:
        print(traceback.format_exc(), "\n\n", "-"*100, "\n\n")
        raise
