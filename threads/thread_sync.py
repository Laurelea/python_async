import logging
import threading
import time


def thread_func(*args):
    thread_name = threading.current_thread().name
    print(f'Поток {thread_name} запустился')

    time.sleep(1)
    print(f'Поток {thread_name} завершился')


if __name__ == '__main__':
    format = '%(asctime)s: %(message)s'
    logging.basicConfig(format=format, level=logging.INFO, datefmt='%H:%M:%S')

    threads = list()
    for idx in range(4):
        logging.info(f'Создан поток {idx}')

        th = threading.Thread(target=thread_func, args=(idx,), name='th-{}'.format(idx))
        threads.append(th)
        th.start()

    for idx, thread in enumerate(threads):
        logging.info(f'Вызов join для потока {idx}')
        thread.join()
        logging.info(f'Поток завершён {idx}')
