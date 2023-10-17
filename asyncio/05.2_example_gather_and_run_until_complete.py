import time
import asyncio

async def greeting(name: str):
    print(f'{time.ctime()} привет, {name}...')
    await asyncio.sleep(1.6)
    print(f'{time.ctime()} пока, {name}...')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pending_tasks = [greeting(name) for name in ('гость', 'пользователь', 'администратор')]
    group_tasks = asyncio.gather(*pending_tasks, return_exceptions=True)
    try:
        loop.run_until_complete(group_tasks)  # цикл остановится самостоятельно
    finally:
        loop.close()
