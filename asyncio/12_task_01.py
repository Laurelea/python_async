"""
Задание 1
Реализуйте работу цикла событий и перехватите системные вызовы SIGINT и SIGTERM для корректного завершения работы.
Используйте метод add_signal_handler() и модуль signal.
"""

import asyncio
import multiprocessing
import random
import signal


async def delay(id, delay):
    print(f'task {id} started...')
    await asyncio.sleep(delay)
    print(f'task {id} stopped...')


async def close_loop(taskssignal, loop):
    print(f'signal {taskssignal}, stopping...')

    pending_tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in pending_tasks:
        print(f'stopping task {task.get_name()}...')
        task.cancel()

    await asyncio.gather(*pending_tasks, return_exceptions=True)

    loop.stop()


def main():
    print(f'Process {multiprocessing.current_process().ident}')

    loop = asyncio.get_event_loop()
    signals = (signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s,
            lambda s=s: asyncio.create_task(close_loop(s, loop))
        )

    tasks = [loop.create_task(delay(i, random.randint(5, 20))) for i in range(1, random.randint(5, 20))]

    group_tasks = asyncio.gather(*tasks, return_exceptions=True)

    try:
        loop.run_until_complete(group_tasks)
    finally:
        loop.close()


if __name__ == '__main__':
    main()
