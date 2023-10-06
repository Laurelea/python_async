import operator

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

    manager.send(None)  # своего рода инициализация
    manager.send((1, 2, operator.add))
    manager.send((100, 20, operator.sub))
    manager.send((5, 15, operator.mul))
    manager.send((None, None, 'h'))
    manager.close()
