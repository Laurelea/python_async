# python 3.9.5

import threading
import time


def func_thread1():
    thread = threading.current_thread()
    print(f'Поток {thread.name} запущен')

    print(f'Поток {thread.name} ожидает получение лок1')
    lock1.acquire()
    print(f'Поток {thread.name} получил лок1, вычисления')
    time.sleep(1)

    print(f'Поток {thread.name} ожидает получение лок2')
    lock2.acquire()
    print(f'Поток {thread.name} получил лок2, вычисления')
    time.sleep(1)

    print(f'Поток {thread.name} разблокировал оба лока')
    lock1.release()
    lock2.release()


def func_thread2():
    thread = threading.current_thread()
    print(f'Поток {thread.name} запущен')

    # первым блокируем блокировку 1, а не блокировку 2, как раньше
    print(f'Поток {thread.name} ожидает получение лок1')
    lock1.acquire()
    print(f'Поток {thread.name} получил лок1, вычисления')
    time.sleep(3)

    # теперь блокируем блокировку 2
    print(f'Поток {thread.name} ожидает получение лок2')
    lock2.acquire()
    print(f'Поток {thread.name} получил лок2, вычисления')
    time.sleep(3)

    print(f'Поток {thread.name} разблокировал оба лока')
    lock2.release()
    lock1.release()


lock1 = threading.Lock()
lock2 = threading.Lock()

thread1 = threading.Thread(name="th-1", target=func_thread1)
thread2 = threading.Thread(name="th-2", target=func_thread2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print('Завершение программы')