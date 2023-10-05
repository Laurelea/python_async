"""
Класс Manager
Класс Manager предоставляет способ создания централизованных объектов Python, которые можно безопасно использовать между
процессами, в том числе по сети между процессами, работающими на разных машинах.
У объекта класса Manager есть методы, которые будут создавать общие объекты и возвращать соответствующие прокси-объекты.
Прокси ссылается на общий объект, который живёт (предположительно) в другом процессе. Общий объект считается референтом
прокси. У некольких прокси-объектов может быть один и тот же референт.
Среди методов объекта класса Manager есть Queue и рассмотренные выше примитивы синхронизации. Они решают те же задачи.
Однако, прокси-объекты сериализуются pickle – их можно передать в дочерний процесс. Разберём разницу на примерах.
Вот такой пример отработает без ошибок, потому что очередь multiprocessing.Queue передается в дочерний процесс при его
создании:

"""

# from multiprocessing import Process, Queue
#
# def producer(queue: Queue):
#     queue.put('Hello')
#     queue.put(None)
#
# def consumer(queue: Queue):
#     while True:
#         item = queue.get()
#         if item is None:
#             break
#         print(f'Получили {item}', flush=True)
#
# if __name__ == '__main__':
#     queue = Queue()
#     consumer_process = Process(target=consumer, args=(queue,))  # очередь передается при создании инстанса
#     consumer_process.start()
#     producer_process = Process(target=producer, args=(queue,))
#     producer_process.start()
#     producer_process.join()
#     consumer_process.join()


"""
Но если передавать очередь в дочерний процесс после его создания, то приложение завершится с ошибкой. 
Это нужно учитывать при использовании multiprocessing.Pool
Ошибка связана с тем, что pickle не может сериализовать объект multiprocessing.Queue, а при передаче в map все 
аргументы сериализуются
"""
#
# from multiprocessing import Pool, Queue
#
# def worker(item: tuple[Queue, int]):
#     queue, index = item
#     queue.put(index)
#     print(f'{index} элемент отправлен в очередь')
#
# if __name__ == '__main__':
#     queue = Queue()
#     items = [(queue, 1), (queue, 2), (queue, 3)]
#     with Pool() as pool:
#         pool.map(worker, items)  # очередь передается как аргумент функции уже после создания инстанса

"""
В этом случае на помощь приходит объект класса Manager:
"""

from multiprocessing import Pool, Queue, Manager

def worker(item: tuple[Queue, int]):
    queue, index = item
    queue.put(index)
    print(f'{index} элемент отправлен в очередь')


if __name__ == '__main__':
    m = Manager()
    queue = m.Queue()
    items = [(queue, 1), (queue, 2), (queue, 3)]
    with Pool() as pool:
        pool.map(worker, items)
        