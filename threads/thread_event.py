import random, time
from threading import Event, Thread

event = Event()

"""
Примитивы синхронизции
Event
Event — простейший механизм связи между потоками: один поток сигнализирует о событии, а другие потоки ждут его.
"""

def waiter(event):
    print('Ожидаю сигнала...')
    event.wait()
    print('Продолжаю выполнение...')
    event.clear()
    print('Waiter завершил работу...')


def trigger(event):
    print('Trigger начал работу...')
    time.sleep(random.randrange(2, 10))
    event.set()
    print('Trigger завершил работу...')


if __name__ == '__main__':
    threads = []
    # Cоздаём поток,который будет ожидать сигнала
    # для продолжения выполнения работы
    th = Thread(target=waiter, args=(event,))
    threads.append(th)
    th.start()
    # Cоздаём поток, который будет сигнализировать
    # о возможности продолжения работы
    th = Thread(target=trigger, args=(event,))
    threads.append(th)
    th.start()

    for thread in threads:
        thread.join()

    print('Все задачи выполнены успешно...')