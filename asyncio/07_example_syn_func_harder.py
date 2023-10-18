import asyncio
import concurrent.futures
import multiprocessing
import threading
import time

import requests

"""
Цикл событий не заблокировался, задача ввода-вывода запустилась в отдельном потоке, а расчетная задача – в отдельном процессе.
"""


def show_identities(name: str):
    print(
        f'Функция: {name} работает в процессе с id: {multiprocessing.current_process().ident}, '
        f'в потоке с id: {threading.current_thread().ident}'
    )


async def greeting(name: str):
    print(f'{time.ctime()} Привет, {name}...')
    await asyncio.sleep(1.6)
    print(f'{time.ctime()} Пока, {name}...')


def blocking_sleep():
    time.sleep(0.7)
    print(f'{time.ctime()} Вызов блокирующего метода в отдельном потоке...')


def fetch_data():
    show_identities('fetch_data')
    response = requests.get('https://yandex.ru/')
    data = response.content
    print(f'{time.ctime()} Получены данные с сайта yandex.ru: ', len(data))


def calculate():
    show_identities('calculate')
    print(f'{time.ctime()} Произведен сложный расчет', sum(i * i for i in range(10 ** 7)))


if __name__ == '__main__':
    show_identities('__main__')

    loop = asyncio.get_event_loop()

    loop.create_task(greeting('гость'))
    loop.create_task(greeting('пользователь'))
    loop.create_task(greeting('администратор'))

    loop.run_in_executor(None, blocking_sleep)

    thread_pool = concurrent.futures.ThreadPoolExecutor()
    loop.run_in_executor(thread_pool, fetch_data)

    proc_pool = concurrent.futures.ProcessPoolExecutor()
    loop.run_in_executor(proc_pool, calculate)

    pending_tasks = asyncio.all_tasks(loop)
    group_tasks = asyncio.gather(*pending_tasks, return_exceptions=True)

    loop.run_until_complete(group_tasks)

    thread_pool.shutdown()
    proc_pool.shutdown()
    loop.close()
