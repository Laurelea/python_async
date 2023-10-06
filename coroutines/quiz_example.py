def coroutine():
    a = yield 47
    b = yield
    yield a + b


if __name__ == '__main__':
    coro = coroutine()
    first = next(coro)
    coro.send(3)
    result = coro.send(first)
    print(result)
