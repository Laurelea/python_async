from functools import wraps
from queue import Queue
from typing import Any, Generator, Callable


def coroutine(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen

    return wrap

@coroutine
def my_func():
    for i in range(3):
        a = yield i
        yield a * 2

f = my_func()

# print(next(f))
print(f.send(5))
next(f)
print(f.send(11))
print(f.send(33))
print(f.send(55))