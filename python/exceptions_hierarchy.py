# -*- coding: utf-8 -*-

import sys
import time

if __name__ == "__main__":
    try:
        # time.sleep(5)
        # sys.exit(1)
        raise ValueError("value")
    except Exception as e:
        print("Catched ValueError!", e)

    try:
        sys.exit(1)
    except Exception:
        print("Catched exit by Exception.")
    except:
        print("Catched exit by empty except")
