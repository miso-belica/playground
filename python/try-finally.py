# -*- coding: utf-8 -*-


def test_finally_beats_return():
    def function():
        try:
            return "try"
        finally:
            return "finally"

    assert function() == "finally"


def test_finally_beats_except():
    def function():
        try:
            raise Exception("intentional")
        except Exception:
            return "try"
        finally:
            return "finally"

    assert function() == "finally"


def test_try_except_finally_else_order_with_exception():
    values = []

    def function():
        try:
            values.append("try-before-exception")
            raise Exception("intentional")
            values.append("try-after-exception")
        except Exception:
            values.append("except")
        else:
            values.append("else")
        finally:
            values.append("finally")

        values.append("end-of-function")

    function()

    assert values == [
        "try-before-exception",
        "except",
        "finally",
        "end-of-function",
    ]


def test_try_except_finally_else_order_without_exception():
    values = []

    def function():
        try:
            values.append("try")
        except Exception:
            values.append("except")
        else:
            values.append("else")
        finally:
            values.append("finally")

        values.append("end-of-function")

    function()

    assert values == [
        "try",
        "else",
        "finally",
        "end-of-function",
    ]


def test_recursive_function_with_finally():
    values = []

    def function(iterations):
        try:
            values.append(f"try {iterations}")
            if iterations > 0:
                raise Exception(f"intentional {iterations}")
        except Exception:
            values.append(f"except {iterations}")
            return function(iterations-1)
        finally:
            values.append(f"finally {iterations}")

    function(2)

    assert values == [
        "try 2",
        "except 2",
        "try 1",
        "except 1",
        "try 0",
        "finally 0",
        "finally 1",
        "finally 2",
    ]
