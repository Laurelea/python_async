import asyncio
from asyncio import Future


async def main():
    my_future = Future()
    print(my_future.done())  # Результат ещё не получен, поэтому Future счиатется невыполненной
    my_future.set_result('Результат')
    print(my_future.done())  # Теперь Future завершена
    print(my_future.result())


asyncio.run(main())
