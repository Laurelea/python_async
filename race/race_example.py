# python 3.9.5

from threading import Thread

# Глобальная переменная, которая будет изменяться из нескольких потоков
counter = 0

def increment():
    global counter
    for _ in range(2000000):
        counter += int(1)

# Создание и запуск потоков
t = Thread(target=increment)
t.start()

t2 = Thread(target=increment)
t2.start()

# Дожидаемся завершения работы потоков
t.join()
t2.join()
print(counter)