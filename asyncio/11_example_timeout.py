import random
import asyncio


async def delay():
    rand_delay = random.uniform(0.3, 1.9)
    print(f'Сгенерировано число {rand_delay}...')
    await asyncio.sleep(rand_delay)
    print(f'Завершилась корутина {rand_delay}...')
    return rand_delay


async def main():
    tasks = [asyncio.create_task(delay()) for _ in range(5)]
    print('Начало работы...')
    # Функция wait() модуля asyncio одновременно запускает объекты классов Future или Task из переданного множества,
    # а затем блокирует выполнение программы до выполнения условия, указанного в аргументе return_when.
    # Затем возвращается кортеж из двух множеств Task/Future в виде done, pending

    # В отличие от функции asyncio.wait_for(), asyncio.wait() не отменяет, а приостанавливает задачи при наступлении
    # таймаута.

    # Аргумент timeout (float или int) указан в секундах. Он используется для управления временем ожидания результатов
    # задач, прежде чем приостановить невыполненные.
    done, pending = await asyncio.wait_for(tasks, return_when=asyncio.FIRST_COMPLETED, timeout=None)

    for task in pending:
        task.cancel()

    completed_task = done.pop()
    print('Результат работы приложения:', completed_task.result())


if __name__ == '__main__':
    asyncio.run(main())
