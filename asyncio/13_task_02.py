"""
Задание 2
Доработайте решение, чтобы через 3 секунды отобразились текущая дата и время.
Для реализации используйте метод call_later().
"""

import asyncio
import random
import signal
import datetime


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
    loop.stop()  # прерываем работу программы


def send_date():
    print(datetime.datetime.now())


async def main():
    loop = asyncio.get_running_loop()
    signals = (signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s,
            lambda s=s: asyncio.create_task(close_loop(s, loop))
        )

    tasks = [loop.create_task(delay(i, random.randint(5, 15))) for i in range(1, random.randint(5, 10))]

    # extra_task = loop.create_task(send_date())
    # tasks.append(extra_task)
    loop.call_later(3, send_date)

    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED, timeout=5)

        for task in pending:
            print(f'stopping task {task.get_name()}...')
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
    except asyncio.CancelledError as error:
        print(error)
        exit(1)


if __name__ == '__main__':
    asyncio.run(main())
