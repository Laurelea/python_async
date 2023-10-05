import threading
import time

thread_lock = threading.Lock()

"""
Класс MyThread запускает блокировку объекта через thread_lock внутри функции run(). Программа исполняет потоки по 
отдельности, и каждый вызов в потоке thread_count_down будет ожидать, когда блокировка будет снята другим потоком.

Используется для защиты от изменения общей переменной одновременно из нескольких потоков.

Как только поток получил блокировку, последующие попытки получить его блокируются, пока поток не будет разблокирован.

Любой поток может снять блокировку

"""


class MyThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):
        print(f'Запущен поток {self.name}')
        thread_lock.acquire()
        # var 1
        '''Из примера'''
        try:
            thread_count_down(self.name, self.delay)
        finally:
            thread_lock.release()
        # end var 1

        # var 2
        '''Непонятно, в чем разница. Непредсказуемость последовательности?'''
        # thread_count_down(self.name, self.delay)
        # thread_lock.release()
        # end var 2
        print(f'Завершен поток {self.name}')


def thread_count_down(name, delay):
    counter = 3

    while counter:
        time.sleep(delay)
        print(f'Поток {name} - {counter}...')
        counter -= 1


if __name__ == '__main__':
    thread1 = MyThread('Thread-1', 0.2)
    thread2 = MyThread('Thread-2', 1)

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    print('Завершаем работу.')
