# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import re
import os
import sys


IGNORE_PATTERN = re.compile(r"\.git|\.svn")


def remove_empty_folders(path):
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files) > 0:
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and not IGNORE_PATTERN.search(path):
        print("Removing empty folder:", path)
        # os.rmdir(path)
    elif contains_only_ignored(files):
        print("!!! With only ignored files:", path)


def contains_only_ignored(files):
    for file in files:
        if not IGNORE_PATTERN.search(path):
            return False

    return True


if __name__ == "__main__":
    remove_empty_folders(sys.argv[1])
