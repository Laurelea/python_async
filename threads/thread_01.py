import time

# Вместо multiprocessing используем threading
from threading import Thread

def printer(name):
    time.sleep(3)
    print('привет', name)

# Интерфейс похож на работу с процессами
t = Thread(target=printer, args=('Алиса',))
t.start()
print('Пока выполняется поток, съешьте ещё этих мягких французских булок да выпейте же чаю ☕️')
# Дождёмся выполнения операции в потоке
t.join()
