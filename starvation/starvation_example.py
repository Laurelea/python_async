from time import sleep
from threading import Thread
from threading import Lock

counter = 0

def task(lock, identifier):
    global counter
    with lock:
        for i in range(5):
            print(f'Поток {identifier} работает')
            temp = counter
            sleep(1)
            temp += 1
            counter = temp

lock = Lock()
threads = [Thread(target=task, args=(lock, i)) for i in range(3)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(counter)