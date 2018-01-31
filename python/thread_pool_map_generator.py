# -*- coding: utf-8 -*-

"""
This is a test of thread pool executor it its map function waits for generator or
it will consume it all and then waits.
"""

import time
from multiprocessing.dummy import Pool


THREADS_COUNT = 3


def main():
    with Pool(THREADS_COUNT) as pool:
        for n in pool.imap_unordered(processor, generator()):
            print("Result", n)


def generator():
    for n in range(10):
        print("Generating", n)
        yield n
        time.sleep(1)


def processor(n):
    print("Processing", n)
    time.sleep(3)
    return n


if __name__ == '__main__':
    main()
