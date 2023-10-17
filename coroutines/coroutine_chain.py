# оригинал: http://www.dabeaz.com/coroutines/trampoline.py
# модификация яп: https://practicum.yandex.ru/learn/async-python/courses/be7a81c7-2443-4476-8813-604159438fcb/sprints/140330/topics/1f018dcf-498d-4ca0-9af2-06bd0f1e4c00/lessons/02b1bc8c-f727-4675-abf9-96ffff01ead2/

# см. также запуск через обертку event_loop/task_with_coroutine_chain.py

def double(x):
    yield x * x


def add(x, y):
    # Передача генератором управления другому генератору
    # https://docs-python.ru/tutorial/generatory-python/vyrazhenie-yield-from-expr/
    # сокращенная форма от:
    # for i in double(x + y):
    #         yield i
    yield from double(x + y)


def main(x, y):
    result = yield add(x, y)
    # эта часть выполнится при следующем вызове
    print(result)
    # завершение работы генератора
    yield


def run():
    m = main(3, 4)
    # получаем встроенный в main генератор, то есть add
    sub = m.send(None)
    # вызываем этот внутренний генератор, получаем результат
    result = sub.send(None)
    # завершаем работу основного генератора
    m.send(result)


run()
