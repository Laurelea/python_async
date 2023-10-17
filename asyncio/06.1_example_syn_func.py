"""
Часто при разработке асинхронного приложения возникает необходимость запустить синхронную функцию.
Обычно такие функции блокируют цикл событий и вся асинхронность пропадает из приложения.
Рассмотрим пример такого неправильного подхода. Для этого в примере выше заменим вызов асинхронного метода asyncio.sleep
на синхронный time.sleep
"""
import time
import asyncio


async def greeting(name: str):
    print(f'{time.ctime()} привет, {name}...')
    time.sleep(1.6)  # sync func
    print(f'{time.ctime()} пока, {name}...')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pending_tasks = [greeting(name) for name in ('гость', 'пользователь', 'администратор')]
    group_tasks = asyncio.gather(*pending_tasks, return_exceptions=True)
    try:
        loop.run_until_complete(group_tasks)
    finally:
        loop.close()
