# -*- coding: utf-8 -*-
import pytest


class AppException(Exception):
    pass


class AppNotWorking(AppException, EnvironmentError):
    """
    This exception should be caught by all parents.
    It's backward compatible with `EnvironmentError` when it's raised.
    """


def test_exception_does_not_catch_its_parent():
    """Exceptions are backward compatible only when raised, not when used in `except`."""
    with pytest.raises(EnvironmentError):
        try:
            raise EnvironmentError
        except AppNotWorking:
            pass


@pytest.mark.parametrize("exception", [AppNotWorking, AppException, EnvironmentError, Exception])
def test_exception_should_be_caught_by_all_parents(exception):
    try:
        raise AppNotWorking
    except exception:
        pass
