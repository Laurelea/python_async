from functools import wraps

def coroutine(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap

@coroutine
def print_name(prefix):
    print(f'Поиск префикса в строке: {prefix}')
    try:
        while True:
            name = yield
            if prefix in name:
                print(name)
    except GeneratorExit:
        print('Закрытие корутины')


if __name__ == '__main__':
    coro = print_name('Привет')
    coro.send('Практикум')
    coro.send('Привет, Практикум')
    coro.send('Hello, Практикум')
    coro.close()
