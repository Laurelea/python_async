"""
Разница с первым вариантом:

В целом, почти разницы нет.
loop.run_until_complete() - это синхронный вызов, который блокирует выполнение до завершения всех задач. В некоторых
случаях это может стать проблемой, если у вас есть другие асинхронные операции, которые должны выполняться параллельно.

Если нужно явное управление асинхронным выполнением и хотите организовать асинхронный код в виде асинхронных функций,
первый вариант может быть более предпочтителен (который с asyncio.run(main())). Если у вас есть смешанный синхронный и
асинхронный код и вам нужно более гибкое управление выполнением, второй вариант может быть более подходящим.
"""


import asyncio
import random
import signal


# os.kill(35387, signal.SIGTERM)


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


async def main():
    loop = asyncio.get_running_loop()
    signals = (signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s,
            lambda s=s: asyncio.create_task(close_loop(s, loop))
        )

    tasks = [loop.create_task(delay(i, random.randint(5, 20))) for i in range(1, random.randint(5, 20))]

    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED, timeout=5)

        for task in pending:
            print(f'stopping task {task.get_name()}...')
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
        # loop.stop() тут это лишнее, потому что вызов через asyncio.run(main()) сам всё закроет
    except asyncio.CancelledError:
        pass
    # finally: тут это лишнее, потому что вызов через asyncio.run(main()) сам всё закроет
    #     loop.close()
    """
    Когда используется asyncio.run(main()), asyncio.run() создает новый цикл событий, запускает вашу функцию main() в 
    этом цикле и автоматически закрывает цикл после завершения функции main(). Поэтому не нужно явно вызывать loop.stop() 
    внутри функции main(). Все необходимые операции с циклом (запуск, ожидание завершения и закрытие) обрабатываются 
    автоматически asyncio.run().
    Добавление loop.stop() в функцию main() может привести к ошибкам, потому что цикл уже будет закрыт asyncio.run()
    """

if __name__ == '__main__':
    asyncio.run(main())
