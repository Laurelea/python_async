# python 3.9.5

import time
import threading
from multiprocessing import Pool

MAX_INT = 500_000_000

def increment(n, m, max):
    while n < max:
        n += m

if __name__ == '__main__':

    # Последовательное выполнение
    start = time.time()
    increment(0, 2, MAX_INT)
    print(f'Последовательный код: {time.time() - start : .2f} s.')
    print()

    # Множество процессов

    pool = Pool(processes=2)
    start = time.time()
    pool.apply_async(increment, args=(0, 2, MAX_INT//2))
    pool.apply_async(increment, args=(MAX_INT//2 + 1, 2, MAX_INT))
    pool.close()
    pool.join()
    print(f'Пул процессов: {time.time() - start : .2f} s.')
    print()

    # Множество потоков

    thread1 = threading.Thread(target=increment, args=(0, 2, MAX_INT//2))
    thread2 = threading.Thread(target=increment, args=(MAX_INT//2 + 1, 2, MAX_INT))
    start = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print(f'Пул потоков: {time.time() - start : .2f} s.')
    print()