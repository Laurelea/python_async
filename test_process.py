
import time
import os

import multiprocessing as mp

def printer(name):
    # Проверим гипотезу и увеличим время выполнения функции, чтобы процесс не завершился раньше
    time.sleep(50)
    print('привет', name)


if __name__ == '__main__':
    mp.set_start_method('fork')

    p = mp.Process(target=printer, args=('Алиса',))
    p.start()
    print('Пока выполняется процесс, съешьте ещё этих мягких французских булок да выпейте же чаю ☕')

    # Выведем Process ID для текущего процесса и для процесса, который только что запустили
    print('Главный PID', os.getpid())
    print('Дочерний PID', p.pid)
    # Дождёмся выполнения процесса
    p.join()