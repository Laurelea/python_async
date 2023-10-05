import threading
from time import sleep
from threading import Thread

lock = threading.Lock()
value = 0


def adder(amount, repeats):
    global value
    for _ in range(repeats):
        tmp = value
        sleep(0)
        tmp = tmp + amount
        sleep(0)
        value = tmp


def subtractor(amount, repeats):
    global value
    for _ in range(repeats):
        tmp = value
        sleep(0)
        tmp = tmp - amount
        sleep(0)
        value = tmp


if __name__ == '__main__':
    adder_thread = Thread(target=adder, args=(1, 10000))
    adder_thread.start()
    subtractor_thread = Thread(target=subtractor, args=(1, 10000))
    subtractor_thread.start()
    adder_thread.join()
    subtractor_thread.join()
    print(f'Результат: {value}')