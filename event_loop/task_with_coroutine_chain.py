#  см.п одробнее про цепочку корутин: coroutines/coroutine_chain.py

from task import Task


def double(x):
    yield x * x


def add(x, y):
    yield from double(x + y)


def main():
    result = yield add(1, 2)
    # эта часть выполнится при следующем вызове
    print(result)
    # завершение работы генератора
    yield


task = Task(main())
task.run()
