# -*- coding: utf-8 -*-

"""
Try this module with:
>>> import callable_module
>>> callable_module("string", 0, 0.0, False, None, jop="hej")
(('string', 0, 0.0, False, None), {'jop': 'hej'})
"""

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys

from types import ModuleType


def __call__(*args, **kwargs):
    return args, kwargs


class CallableModule(ModuleType):
    def __init__(self, original_module):
        super(CallableModule, self).__init__(original_module.__name__)
        self._original_module = original_module

    def __call__(self, *args, **kwargs):
        return self._original_module.__call__(*args, **kwargs)

    def __getattribute__(self, item):
        if item in ("__call__", "_original_module"):
            return object.__getattribute__(self, item)
        else:
            return getattr(self._original_module, item)

sys.modules[__name__] = CallableModule(sys.modules[__name__])


if __name__ == "__main__":
    pass
