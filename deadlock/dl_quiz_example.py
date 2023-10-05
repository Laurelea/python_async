from threading import current_thread
from threading import Thread


def task(other):
    other.join()
    print('Завершение работы')


main_thread = current_thread()
new_thread = Thread(target=task, args=(main_thread,))
new_thread.start()
task(new_thread)

