"""
Библиотека multiprocessing предоставляет класс Pool для упрощения обработки параллельных задач:
"""

import multiprocessing


def calculate_func(data):
    result = data * 2 + 44
    return f'{data}: {result}'


if __name__ == '__main__':
    inputs = list(range(0, 100))
    pool = multiprocessing.Pool(processes=3 )
    # Параметр processes - опционален, по умолчанию используется значение os.cpu_count()

    pool_outputs = pool.map(calculate_func, inputs)
    pool.close()
    pool.join()
    print('Pool:', pool_outputs)
