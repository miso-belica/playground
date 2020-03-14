# -*- coding: utf-8 -*-

"""
https://github.com/pytest-dev/pytest/issues/3962
https://stackoverflow.com/a/54454931/2988107
https://github.com/pytest-dev/pytest/blob/master/src/_pytest/assertion/truncate.py#L33
"""

import os

# this is needed to force pytest to show full diff even if the console output is not verbose
os.environ["CI"] = '1'

_EXPECTED_DICT = {
    "numbers": list(range(100)),
    **{i: f"{i}. value" for i in range(100)},
}


def test_compare_big_dicts():
    dictionary = {k: v for k, v in _EXPECTED_DICT.items() if not isinstance(k, int) or k % 5 != 0}
    dictionary = {k: (v if not isinstance(k, int) or k % 9 != 0 else "I got you") for k, v in dictionary.items()}
    dictionary["numbers"] = [n for n in dictionary["numbers"] if n % 30 != 0]

    assert dictionary == _EXPECTED_DICT
