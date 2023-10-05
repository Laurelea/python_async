import random
import time
from threading import Condition, Thread

condition = Condition()
data_pool = []

"""
Примитивы синхронизции
Condition
Condition — условие, которые позволяют одному или нескольким потокам ждать, пока их не уведомит другой поток о 
своём выполнении. 
"""

def producer(data_pool, pool_size):
    for i in range(pool_size):
        time.sleep(random.randrange(2, 5))
        # Блокируем потоки, подписанные на условие
        condition.acquire()
        num = random.randint(100, 500)
        data_pool.append(num)
        # Сигнализируем о возможности продолжить работу
        # При замене на .notify_all(), сигнал о продолжении получат все потоки,
        # подписанные и ожидающие текущий триггер
        condition.notify()
        print('Отправлено:', num)
        condition.release()


def consumer(data_pool, pool_size):
    for i in range(pool_size):
        # Блокируем потоки, подписанные на условие
        condition.acquire()
        # Ожидание сигнала о возможности продолжения работы
        condition.wait()
        time.sleep(5)
        print('%s: Получено: %s' % (time.ctime(), data_pool.pop()))
        condition.release()


if __name__ == '__main__':
    threads = []
    threads_max = random.randrange(2, 7)

    for func in [producer, consumer]:
        th = Thread(target=func, args=(data_pool, threads_max))
        threads.append(th)
        th.start()

    for thread in threads:
        thread.join()

    print('Все задачи выполнены успешно...')

