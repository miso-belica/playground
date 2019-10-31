# -*- coding: utf-8 -*-

import random
from itertools import permutations
from operator import itemgetter

import pytest


def test_snippets():
    """
    What is the output of the following Python snippets?

    >>> ''.join(range(5))

    >>> A = 0
    >>> A or None

    >>> d = {'one': 1, 'two': 2}
    >>> d.pop('two', True)
    """
    with pytest.raises(TypeError):
        ''.join(range(5))

    assert (0 or None) is None

    assert {'one': 1, 'two': 2}.pop('two', True) == 2


def test_all_true():
    """
    Fill in the blanks with the same code to make both lines return True!

    >>> A = True
    >>> B = False
    A __________ = 1
    B __________ = 0
    """
    a = True
    b = False

    assert a + 0 == 1
    assert b + 0 == 0


@pytest.mark.parametrize("a,b", [
    (None, None),
    (None, object()),
    (object(), None),
    (object(), object()),
])
def test_fewer_characters(a, b):
    """How do you write "result = A if A else B" in fewer characters?"""
    assert (a if a else b) is (a or b)


def test_dict_swap_keys_with_values():
    """
    How do you transform a given dict to the dict where its values are keys and its keys are values?
    >>> d = {'one': 1, 'two': 2}
    """
    d = {'one': 1, 'two': 2}

    assert {v: k for k, v in d.items()} == {1: 'one', 2: 'two'}


def test_dashes_with_few_characters():
    """How do you print a line with 80 dashes using fewer than 20 characters in the code."""
    assert "-" * 80 == "--------------------------------------------------------------------------------"


def test_dict_keys_sorted_by_values():
    """
    How do you create a list of keys from a dictionary in one line, sorted by their associated value?
    >>> d = {'one': 1, 'eleven': 11}
    """
    d = {'one': 1, 'eleven': 11}

    assert [k for k, _ in sorted(d.items(), key=itemgetter(1))] == ["one", "eleven"]


def test_the_cheapest_flights():
    """
    You have 2 groups of flights, each group has 600 flights in it.
    In one, you have flights from A to B on one date.
    In the other you have flights from B to A on another date.
    Both groups are unsorted and all flights have different prices.

    Task:
    Find the 50 cheapest combinations with the lowest possible complexity.
    """
    group_1 = _generate_random_group()
    group_2 = _generate_random_group()


def _generate_random_group():
    flights_count = 600

    group = set()
    while len(group) != flights_count:
        price = random.uniform(10, 10_000)
        group.add(price)

    return group


def test_sum_of_digits():
    """
    Calculate the sum of all 3 digit numbers consisting of digits 1, 2 and 3 (where you can use each
    digit only once) that are divisible by 3.
    """
    numbers = [int("".join(n)) for n in permutations("123")]
    # all numbers are divisible by 3 because the sum of all digits "1 + 2 + 3" is divisible by 3 :)
    # numbers = list(filter(lambda n: n % 3 == 0, numbers))

    assert numbers == [123, 132, 213, 231, 312, 321]
    assert sum(numbers) == 1332
