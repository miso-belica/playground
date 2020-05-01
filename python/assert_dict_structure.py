# -*- coding: utf-8 -*-

"""
https://dev.to/misobelica/any-advanced-alternative-to-unitest-mock-any-lkh
"""

from typing import Any, Callable
from unittest.mock import ANY

import pytest


def test_chatbot_response_is_polite():
    data = generate_data()

    assert data == {
        "id": ANY,
        "confidence": pytest.approx(0.5, abs=0.5),
        "text": "Hi, I am chatbot :)",
        "responses": ExpectPredicate(lambda r: isinstance(r, list) and all(isinstance(i, str) for i in r)),
    }


class ExpectPredicate:
    def __init__(self, predicate: Callable[[Any], bool]):
        self._predicate = predicate

    def __eq__(self, other):
        return self._predicate(other)


def generate_data():
    return {
        "id": "123",
        "confidence": 0.89,
        "text": "Hi, I am chatbot :)",
        "responses": ["1", "2", "3"],
    }
