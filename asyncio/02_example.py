"""
- Метод с async может содержать вызовы с await, return или yield.
- Использование yield в сопрограмме создает генератор, который можно использовать с помощью async for.
- Контекстные менеджеры могут быть использованы в сопрограммах через конструкцию async with.
- Определение вызова с await требует использования awaitable-объекта: им может быть корутина или объект, с определенным
 методом __await__().
"""

import asyncio
import random

# Функция, определенная через async, является корутиной (сопрограммой)
async def aget_random():
    r = random.random()
    await asyncio.sleep(r)
    return r

def get_random():
    return random.random()

if __name__ == "__main__":
    print(type(get_random()))

    # тут возвращает саму корутину
    result = aget_random()
    # а тут её результат
    asyncio.run(result)
    print(type(result))
