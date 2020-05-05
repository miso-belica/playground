# -*- coding: utf-8 -*-

"""
This is a test of process pool and how different methods exits the processes.
"""

import time
from contextlib import closing
from multiprocessing import Pool


PROCESSES_COUNT = 2


def main_context_manager():
    results = []
    with Pool(PROCESSES_COUNT) as pool:
        for n in range(PROCESSES_COUNT):
            results.append(pool.apply_async(processor, args=(n, )))

    pool.join()

    for result in results:
        print(result.ready())


def main_terminate():
    results = []
    pool = Pool(PROCESSES_COUNT)
    for n in range(PROCESSES_COUNT):
        results.append(pool.apply_async(processor, args=(n, )))

    pool.terminate()
    pool.join()

    for result in results:
        print(result.ready())


def main_close():
    results = []
    pool = Pool(PROCESSES_COUNT)
    for n in range(PROCESSES_COUNT):
        results.append(pool.apply_async(processor, args=(n, )))

    pool.close()
    pool.join()

    for result in results:
        print(result.ready())


def main_with_closing():
    results = []
    with closing(Pool(PROCESSES_COUNT)) as pool:
        for n in range(PROCESSES_COUNT):
            results.append(pool.apply_async(processor, args=(n, )))

    pool.join()

    for result in results:
        print(result.ready())


def processor(n):
    print("Processing", n)
    time.sleep(3)
    return n


if __name__ == '__main__':
    main_context_manager()
    main_terminate()
    main_close()
    main_with_closing()
