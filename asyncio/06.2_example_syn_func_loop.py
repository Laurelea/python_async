"""
Посмотрим на возможность запуска блокирующей операции в рамках цикла событий.
Немного изменим предыдущий пример – для наглядности вынесем блокирующую операцию в отдельную функцию:
"""
import time
import asyncio
import threading


async def greeting(name: str):
    print(f'{time.ctime()} Привет, {name}...')
    await asyncio.sleep(1.6)
    print(f'{time.ctime()} Пока, {name}...')

def blocking_sleep():
    time.sleep(0.7)
    print(f'{time.ctime()} Вызов блокирующего метода в отдельном потоке...')
    print('Поток блокирующего метода', threading.current_thread())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(greeting('гость'))
    loop.create_task(greeting('пользователь'))
    loop.create_task(greeting('администратор'))

    # run_in_executor организует вызов функции func в указанном исполнителе executor. Этот метод возвращает объект Future.
    # Аргумент executor должен быть экземпляром concurrent.futures.Executor.
    # Если в качестве исполнителя передано None, то используется executor по умолчанию.
    loop.run_in_executor(None, blocking_sleep)
    # Исполнителем может быть пул потоков для задач ввода-вывода, или пул процессов для CPU-bound задач.
    # Исполнитель по умолчанию устанавливается методом loop.set_default_executor(executor),
    # параметр executor должен быть экземпляром ThreadPoolExecutor.

    pending_tasks = asyncio.all_tasks(loop)
    group_tasks = asyncio.gather(*pending_tasks, return_exceptions=True)

    print('Основной поток', threading.current_thread())

    loop.run_until_complete(group_tasks)
    loop.close()
