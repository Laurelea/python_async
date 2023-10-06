'''
Использование подобного декоратора при работе с корутинами – хорошая и распространенная практика,
которая избавляет от лишнего кода, нужного для инициализации корутины.
'''

from functools import wraps
import operator


def coroutine(f):
    @wraps(f)  # https://docs.python.org/3/library/functools.html#functools.wraps
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen

    return wrap


@coroutine
def func_manager():
    history = []
    while True:
        x, y, func = yield
        if func == 'h':
            print(history)
            continue
        result = func(x, y)
        print(result)
        history.append(result)


if __name__ == '__main__':
    manager = func_manager()
    print(type(manager))

    manager.send((1, 2, operator.add))
    manager.send((100, 20, operator.sub))
    manager.send((5, 15, operator.mul))
    manager.send((None, None, 'h'))
    manager.close()
