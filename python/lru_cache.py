# -*- coding: utf-8 -*-

"""
I wanted to know how the LRU cache behaves when there is limit and the cache decorator is shared between more methods.
It's because I want to have `@service` decorator to decorate all functions that setups the services and returns it.
I was afraid the cache is shared between functions and if I call another it will the remove the 1st one, ...
"""

from functools import lru_cache


def test_cache_single_service():
    service = lru_cache(maxsize=1)

    @service
    def service1():
        service1._counter = getattr(service1, "_counter", 0) + 1
        return service1._counter

    assert service1.cache_info()._asdict() == {"misses": 0, "hits": 0, "currsize": 0, "maxsize": 1}
    assert service1() == 1
    assert service1.cache_info()._asdict() == {"misses": 1, "hits": 0, "currsize": 1, "maxsize": 1}
    assert service1() == 1
    assert service1.cache_info()._asdict() == {"misses": 1, "hits": 1, "currsize": 1, "maxsize": 1}


def test_cache_more_services():
    service = lru_cache(maxsize=1)

    @service
    def service1():
        service1._counter = getattr(service1, "_counter", 0) + 1
        return service1._counter

    @service
    def service2():
        service2._counter = getattr(service2, "_counter", 0) + 1
        return service2._counter

    @service
    def service3():
        service3._counter = getattr(service3, "_counter", 0) + 1
        return service3._counter

    assert service1.cache_info()._asdict() == {"misses": 0, "hits": 0, "currsize": 0, "maxsize": 1}
    assert service1() == 1
    assert service1.cache_info()._asdict() == {"misses": 1, "hits": 0, "currsize": 1, "maxsize": 1}
    assert service2() == 1
    assert service3() == 1
    assert service1() == 1
    assert service1.cache_info()._asdict() == {"misses": 1, "hits": 1, "currsize": 1, "maxsize": 1}
    assert service2() == 1
    assert service3() == 1


def test_cache_more_services_with_zero_size():
    service = lru_cache(maxsize=0)

    @service
    def service1():
        service1._counter = getattr(service1, "_counter", 0) + 1
        return service1._counter

    assert service1.cache_info()._asdict() == {"misses": 0, "hits": 0, "currsize": 0, "maxsize": 0}
    assert service1() == 1
    assert service1.cache_info()._asdict() == {"misses": 1, "hits": 0, "currsize": 0, "maxsize": 0}
    assert service1() == 2
    assert service1.cache_info()._asdict() == {"misses": 2, "hits": 0, "currsize": 0, "maxsize": 0}
