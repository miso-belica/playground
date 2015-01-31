# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import re


def test_texts_comparisons():
    text1 = "nejaký text: ľščťžýáíé\n"
    assert isinstance(text1, str)
    assert isinstance(text1.encode("utf-8"), bytes)

    text2 = text1.encode("utf-8")
    assert isinstance(text2, bytes)
    assert isinstance(text2.decode("utf-8"), str)

    assert text1 == text2.decode("utf-8")
    assert text1.encode("utf-8") == text2
    assert text1 != text2


def test_regexp_execution():
    WORD_BOUNDARY_PATTERN = re.compile(r'[\W_]+', re.UNICODE)
    splitter = WORD_BOUNDARY_PATTERN.split
    string = 'XaX##XbľščťžýáíéX##XcbůěX#XdľščšťľX'

    assert splitter(string) == ['XaX', 'XbľščťžýáíéX', 'XcbůěX', 'XdľščšťľX']
    try:
        splitter(string.encode("utf-8")) == ['XaX', 'XbľščťžýáíéX', 'XcbůěX', 'XdľščšťľX']
        assert False, "This should not happen :)"
    except TypeError as e:
        assert e.args[0] == "can't use a string pattern on a bytes-like object"


def test_concatenate_bytes():
    try:
        b'abcd' + 'efgh'
        assert False, "This should not happen :)"
    except TypeError as e:
        assert e.args[0] == "can't concat bytes to str"


def test_join_text():
    list = [u'A', u'B', u'C', u'D', u'€ vs. $', u'E', u'F', u'G', u'H']
    assert "ABCD€ vs. $EFGH" == u"".join(list)

    try:
        b''.join(list)
        assert False, "This should not happen :)"
    except TypeError as e:
        expected_error = (
            "sequence item 0: expected bytes, bytearray, "
            "or an object with the buffer interface, str found"
        )
        assert expected_error == e.args[0]


if __name__ == '__main__':
    test_texts_comparisons()
    test_regexp_execution()
    test_concatenate_bytes()
    test_join_text()
