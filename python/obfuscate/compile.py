# -*- coding: utf-8 -*-

import os
from pathlib import Path

if __name__ == "__main__":
    os.system("python -m compileall -qb test.py")
    py_file = Path("test.py").rename("__hidden.py")
    pyc_file = Path("test.pyc").rename("test.py")

    os.system("python test.py")

    pyc_file.unlink()
    path = py_file.rename("test.py")
