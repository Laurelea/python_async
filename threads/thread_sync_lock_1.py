from threading import Thread, Lock
import time

counter = 0


def increase(lock):
    global counter
    lock.acquire()
    local_counter = counter
    local_counter += 1
    time.sleep(0.1)
    counter = local_counter
    lock.release()
    print(f'counter now: {counter}')


if __name__ == '__main__':
    lock = Lock()
    threads = []
    for _ in range(10):
        t = Thread(target=increase, args=(lock,))
        t.start()
        threads.append(t)
    [t.join() for t in threads]
    print(counter)
