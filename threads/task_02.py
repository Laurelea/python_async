from concurrent.futures import ThreadPoolExecutor

data = range(1, 10)
pool_size = 5


def f1(item):
    # Возведение в квадрат
    return item ** 2


def f2(data):
    # Подсчёт суммы элементов массива
    return sum(data)


def worker(data):
    """
    Возведение всех элементов массива в квадрат и
    подсчёт суммы всех элементов
    """
    result = 0
    with ThreadPoolExecutor(max_workers=pool_size) as pool:
        # Взаимодействие с пулом для возведения в квадрат и подсчёта суммы всех элементов
        # squares = [_ for _ in pool.map(f1, data)]
        squares = pool.map(f1, data)
        result = pool.submit(f2, squares).result()
        print(result)

    return result


worker([1, 2, 3])
