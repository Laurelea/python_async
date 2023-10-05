from threading import Timer
import random

"""
Примитивы синхронизции
Timer
Timer определяет механизм отложенного запуска выполнения задач. При создании указывается функция, которая будет 
выполнена после указанного в interval времени. Если необходимо остановить таймер, то нужно вызвать метод cancel().
"""


def logger(msg):
    print(f'Запись в журнал: {msg}')


def reject(timer):
    timer.cancel()
    print('Таймер отменен...')


if __name__ == '__main__':
    tasks = []
    delay = random.randrange(1, 7)
    timer1 = Timer(interval=delay, function=logger, args=(f'Запуск функции после задержки {delay} сек...',))
    timer1.start()
    tasks.append(timer1)

    timer2 = Timer(interval=3, function=logger, args=('Второй таймер с сообщением',))
    timer2.start()
    tasks.append(timer2)

    rejecter = Timer(interval=5, function=reject, args=(timer2,))
    rejecter.start()
    tasks.append(rejecter)

    # for t in tasks:
    #     t.join()

    print('Программа завершена...')