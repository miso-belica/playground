# -*- coding: utf-8 -*-
from contextlib import suppress
from typing import Dict, Iterable, Iterator, List, Optional, TypeVar

import pytest


def test_find_all_mistakes():
    """
    Find all mistakes in function "counts".

    def counts(items, data={}: Dict[str, int]) -> Dict[str, float]:
        for i in items:
            val = items.get(i)
            try:
                data[val] = data[ val ] + 1
            except KeyError, IndexError:
                data[val] = 1
        return data
    """

    def counts(items: Iterable[str]) -> Dict[str, int]:
        data = {}
        for val in items:
            data[val] = data.get(val, 0) + 1

        return data

    assert counts('1,2,2,6,3,2,3'.split(',')) == {'1': 1, '2': 3, '3': 2, '6': 1}
    assert counts('3,1,1,2,3,1,1'.split(',')) == {'1': 4, '2': 1, '3': 2}


def test_write_better_function_count():
    """
    Write simpler and more optimized implementation of the function "counts" so that tests pass.
    """
    from collections import Counter as counts

    assert counts('1,2,2,6,3,2,3'.split(',')) == {'1': 1, '2': 3, '3': 2, '6': 1}
    assert counts('3,1,1,2,3,1,1'.split(',')) == {'1': 4, '2': 1, '3': 2}


def merge_lists(s1: List[int], s2: List[int]) -> List[int]:
    index_1 = 0
    index_2 = 0
    result = []

    while index_1 < len(s1) and index_2 < len(s2):
        item_1 = s1[index_1]
        item_2 = s2[index_2]

        if item_1 <= item_2:
            result.append(item_1)
            index_1 += 1
        if item_2 <= item_1:
            result.append(item_2)
            index_2 += 1

    return result + s1[index_1:] + s2[index_2:]


def merge_iterators(s1: Iterable[int], s2: Iterable[int]) -> List[int]:
    s1 = iter(s1)
    item_1 = _iter_try_next(s1)
    s2 = iter(s2)
    item_2 = _iter_try_next(s2)

    result = []
    while item_1 is not None and item_2 is not None:
        if item_1 <= item_2:
            result.append(item_1)
            item_1 = _iter_try_next(s1)
        elif item_2 < item_1:
            result.append(item_2)
            item_2 = _iter_try_next(s2)

    if item_1:
        result.append(item_1)
    if item_2:
        result.append(item_2)

    return result + list(s1) + list(s2)


T = TypeVar('T')


def _iter_try_next(i: Iterator[T]) -> Optional[T]:
    with suppress(StopIteration):
        return next(i)


@pytest.mark.parametrize("merge", [merge_lists, merge_iterators])
def test_merge_sorted_lists_without_builtins(merge):
    """
    Assume we have two sorted lists. Write the algorithm that merges them
    into one sorted list without usage if the "built-in" functions (sorted etc.).

    Bonus: Our consultants forget to sort the lists sometimes, let them know :)
    Extra bonus: The function accepts iterators too except of the lists.

    >>> def merge(s1: List[int], s2: List[int]) -> List[int]:
    """
    s1 = [1, 2, 2, 4, 4, 8, 9]
    s2 = [1, 2, 2, 3, 5, 6, 7, 7]

    assert merge(s1, s2) == sorted(s1 + s2)
    assert merge([], []) == []
    assert merge([1], []) == [1]
    assert merge([], [1]) == [1]
