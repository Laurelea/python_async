import time
import asyncio

"""
Рекомендуется использовать asyncio.run() вместо комбинации asyncio.get_event_loop() и asyncio.run_until_complete(). 
Заметим, что этот метод создаёт новый цикл каждый раз при вызове и очищает его после завершения.
"""

async def greeting(name: str):
    print(f'{time.ctime()} Привет, {name}...')
    await asyncio.sleep(1.6)
    print(f'{time.ctime()} Пока, {name}...')
    event_loop = asyncio.get_event_loop()
    event_loop.stop()  # Необходимо явно вызвать stop для остановки цикла событий

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(greeting('гость'))
    loop.create_task(greeting('пользователь'))
    loop.create_task(greeting('администратор'))
    try:
        loop.run_forever()
    finally:
        loop.close()
