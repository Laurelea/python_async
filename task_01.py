from multiprocessing import Process, Queue


class Worker(Process):
    def __init__(self, func, func_args, queue):
        super().__init__()
        self.queue = queue
        self.func = func
        self.func_args = func_args

    def run(self):
        # Вызов передаваемого метода и заполнение очереди
        res = self.func(*self.func_args)  # tuple expand (args)
        self.queue.put(res)


def foo(a: int, b: int) -> int:
    return a + b


q = Queue()
worker = Worker(foo, (1, 2), q)
worker.start()
worker.join()

while message := q.get():
    print(message)
