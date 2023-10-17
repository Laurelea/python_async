from task import Task
from scheduler import Scheduler
from typing import Generator

"""
Осталось разобраться с конструкцией SystemCall. Так как изначально цикл событий больше напоминает работу ОС, должен быть
 механизм прерываний, чтобы передать управление ОС. В асинхронном коде прерывание обеспечивается с помощью yield. 
 После переключения контекста может вызываться системная функция для исполнения. Например, для создания новых задач 
 можно использовать вот такой код:
"""


class SystemCall:
    def handle(self, sched: Scheduler, task: Task):
        pass

"""
Интерфейс для создания новых задач в цикле событий
Такой интерфейс позволяет абстрагировать клиентский код. Другими словами, это эмуляция защищённой среды ОС, 
когда последняя предоставляет безопасные методы для работы с ядром.
Такие методы не дают клиентскому коду мешать другим программам в ОС.
"""


class NewTask(SystemCall):
    def __init__(self, target: Generator):
        self.target = target

    def handle(self, sched: Scheduler, task: Task):
        tid = sched.add_task(self.target)
        task.sendval = tid
        sched.schedule(task)