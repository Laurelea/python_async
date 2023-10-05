# python 3.9.5

from threading import Thread, Lock

counter = 0

# Объект блокировки
lock = Lock()

def increment():
    global counter
    for _ in range(2000000):
        # С помощью контекстного менеджера захватываем блокировку
        # и отпускаем, как только выходим из него
        with lock:
            counter += int(1)

    # ещё вариант использования lock:
    # for _ in range(2000000):
    #     lock.acquire()
    #     tmp = counter
    #     sleep(0)
    #     tmp = tmp + amount
    #     sleep(0)
    #     counter = tmp
    #     lock.release()

t = Thread(target=increment)
t.start()

t2 = Thread(target=increment)
t2.start()

t.join()
t2.join()
print(counter)