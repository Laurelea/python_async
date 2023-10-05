from random import randrange
from threading import Barrier, Thread
from time import ctime, sleep


participants = ['Борис', 'Олег', 'Слава', 'Петр']
threads_count = len(participants)
b = Barrier(threads_count)

"""
Примитивы синхронизции
Barrier
Barrier предоставляет примитив для использования фиксированного числа потоков, которым необходимо ждать друг друга.
"""


def start_game():
    player = participants.pop()
    sleeping_time = randrange(1, 10)
    print('Игрок {} начал и ожидает: {}'.format(player, sleeping_time))
    sleep(sleeping_time)
    print('Игрок {} завершил: {}'.format(player, ctime()))
    b.wait()


if __name__ == '__main__':
    threads = []
    print('Начало игры...')
    for i in range(threads_count):
        th = Thread(target=start_game)
        threads.append(th)
        th.start()

    for thread in threads:
        thread.join()
    print('Игра окончена')

