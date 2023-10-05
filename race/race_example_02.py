# python 3.9.5

from threading import Thread

# Глобальная переменная, которая будет изменяться из нескольких потоков
counter = 0

# Допустим, функция запущена в двух потоках
def increment():
    global counter
    for _ in range(2000000):
        # Сначала в буфер копируется значение переменной counter
        # Допустим, текущее значение counter — 100
        # В обоих потоках в переменную buf запишется значение 100
        buf = counter
        # Оба потока увеличивают значение буфера и получают 101
        # У каждого потока своя переменная buf
        buf = buf + 1
        # Оба потока сохраняют переменную buf в counter
        # В итоге counter будет равен 101, а не 102
        counter = buf

# Создание и запуск потоков
t = Thread(target=increment)
t.start()

t2 = Thread(target=increment)
t2.start()

# Дожидаемся завершения работы потоков
t.join()
t2.join()
print(counter)