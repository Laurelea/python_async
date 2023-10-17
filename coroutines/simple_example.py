def coroutine():
    a = None
    b = None
    a = yield 47  # 12 first = next(coro) попадает сюда. функция возвращает 47
    print(f'a is now {a}. b is now {b}')  # 13 coro.send(3) попадает сюда. a присваивается то, что было отправлено, то есть 3. Выводится принт.
    b = yield  # 14  result = coro.send(first) попадает сюда. b присваивается то, что было отправлено, то есть 47. Выводится принт. Возращается конечный результат.
    print(f'a is now {a}. b is now {b}')
    yield a + b

if __name__ == '__main__':
    coro = coroutine()
    first = next(coro)          # first = 47
    coro.send(3)                # a=3
    result = coro.send(first)   # b=47
    print(result)               #