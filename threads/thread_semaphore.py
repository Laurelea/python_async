import random, time
from threading import BoundedSemaphore, Thread

MAX_ITEMS = 8
manager = BoundedSemaphore(MAX_ITEMS)

"""
Примитивы синхронизции
Semaphore
Semaphore — управление атомарным счётчиком, который может увеличиваться или уменьшаться.
"""


def producer(iters_count):
    for i in range(iters_count):
        time.sleep(random.randrange(2, 5))

        print('Producer-{}, {}'.format(i, time.ctime()), end=': ')
        try:
            # Увеличиваем значение счётчика семафора
            manager.release()
            print('Producer завершен.')
        except ValueError:
            print('Пул заполнен, пропускаю...')


def consumer(iters_count):
    for i in range(iters_count):
        time.sleep(random.randrange(2, 5))

        print('Consumer-{}, {}'.format(i, time.ctime()), end=': ')
        # Уменьшение счётчика семафора, разблокировка потока
        if manager.acquire(False):
            print('Consumer завершен...')
        else:
            print('Нечего делать, пропускаю...')


if __name__ == '__main__':
    print('Начало обработки... ')

    threads = []
    loop_range = random.randrange(3, 6)
    print('Всего элементов = %s...' % MAX_ITEMS)

    threads.append(Thread(target=producer, args=(loop_range,)))
    threads.append(Thread(target=consumer, args=(random.randrange(loop_range, loop_range + MAX_ITEMS + 2),),))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print('Работа завершена...')

