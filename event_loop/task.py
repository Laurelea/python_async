import types
from typing import Generator
from systemcall import SystemCall

# Сама по себе задача — обёртка над корутиной.
class Task:
    task_id = 0

    def __init__(self, target: Generator):
        Task.task_id += 1
        self.tid = Task.task_id  # Task ID
        self.target = target  # Target coroutine - функция-генератор, которуюп ередали в таск для исполнения
        self.sendval = None  # Value to send
        self.stack = []  # Call stack

    # Run a task until it hits the next yield statement
    # Умеет обрабатывать цепочку вложенных корутин. Выполняет всё сразу и завершается.
    # Никуда не отдаёт управление
    def run(self):
        while True:
            try:
                result = self.target.send(self.sendval)

                # Этот кусок должен передавать управление ОС?
                if isinstance(result, SystemCall):
                    return result

                if isinstance(result, types.GeneratorType):
                    self.stack.append(self.target)
                    self.sendval = None
                    self.target = result
                else:
                    if not self.stack:
                        return
                    self.sendval = result
                    self.target = self.stack.pop()

            except StopIteration:
                if not self.stack:
                    raise
                self.sendval = None
                self.target = self.stack.pop()
