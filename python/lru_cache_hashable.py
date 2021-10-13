from functools import lru_cache

import pytest


@pytest.mark.parametrize("collection", [
    (1, 2, 3),
    [1, 2, 3],
    {1, 2, 3},
    frozenset({1, 2, 3}),
    {1: 1, 2: 2, 3: 3},
])
def test_lru_cache_limitation(collection):
    cached = lru_cache(maxsize=1)

    @cached
    def function():
        function._counter = getattr(function, "_counter", 0) + 1
        return function._counter

    assert function.cache_info()._asdict() == {"misses": 0, "hits": 0, "currsize": 0, "maxsize": 1}
    assert function() == 1
    assert function.cache_info()._asdict() == {"misses": 1, "hits": 0, "currsize": 1, "maxsize": 1}
    assert function() == 1
    assert function.cache_info()._asdict() == {"misses": 1, "hits": 1, "currsize": 1, "maxsize": 1}
