import logging
from typing import Generator, Union
from queue import Queue
from task import Task
from systemcall import SystemCall
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE # для I/O

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.ready = Queue()
        self.selector = DefaultSelector()  # для I/O
        self.task_map = {}

    def add_task(self, coroutine: Generator) -> int:
        new_task = Task(coroutine)
        self.task_map[new_task.tid] = new_task
        self.schedule(new_task)
        return new_task.tid

    def exit(self, task: Task):
        logger.info('Task %d terminated', task.tid)
        del self.task_map[task.tid]

    def schedule(self, task: Task):
        self.ready.put(task)

    def _run_once(self):
        task = self.ready.get()
        try:
            result = task.run()
            if isinstance(result, SystemCall):
                result.handle(self, task)
                return
        except StopIteration:
            self.exit(task)
            return
        self.schedule(task)

    def event_loop(self):
        while self.task_map:
            self._run_once()

    # I/O waiting
    """
    По сути, event_loop должен предоставлять интерфейс для работы с сокетами. Таких метода всего четыре:
        wait_for_read,
        wait_for_write,
        _remove_reader,
        _remove_writer.
    Эти методы позволяют работать с циклом событий, встроенным в ОС.
    """

    """
    Работа с I/O для цикла событий — «пристройка сбоку» для обработки сетевых запросов. 
    То есть основное назначение цикла событий в Python — обработка функций корутин, которые могут никуда не ходить по 
    сети, а работать только с файловой системой.
    """

    # Расширение планировщика для работы с I/O-задачами
    # регистрирует задачу task для ожидания события чтения на файловом дескрипторе fd.
    def wait_for_read(self, task: Task, fd: int):
        try:
            # Если файловый дескриптор еще не был зарегистрирован, он регистрируется событием чтения.
            key = self.selector.get_key(fd)
        except KeyError:
            # Если файловый дескриптор уже был зарегистрирован, маска событий обновляется для включения события чтения.
            self.selector.register(fd, EVENT_READ, (task, None))

        else:
            mask, (reader, writer) = key.events, key.data
            self.selector.modify(fd, mask | EVENT_READ, (task, writer))

    def wait_for_write(self, task: Task, fd: int):
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            self.selector.register(fd, EVENT_WRITE, (None, task))

        else:
            mask, (reader, writer) = key.events, key.data
            self.selector.modify(fd, mask | EVENT_WRITE, (reader, task))

    # убирает ожидающую задачу чтения для файлового дескриптора fd.
    def _remove_reader(self, fd: int):
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            pass
        else:
            mask, (reader, writer) = key.events, key.data
            mask &= ~EVENT_READ
            if not mask:
                # Если больше нет ожидающих событий чтения для этого дескриптора, он удаляется из планировщика.
                self.selector.unregister(fd)
            else:
                self.selector.modify(fd, mask, (None, writer))

    def _remove_writer(self, fd: int):
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            pass
        else:
            mask, (reader, writer) = key.events, key.data
            mask &= ~EVENT_WRITE
            if not mask:
                self.selector.unregister(fd)
            else:
                self.selector.modify(fd, mask, (reader, None))

    def io_poll(self, timeout: Union[None, float]):
        events = self.selector.select(timeout)
        for key, mask in events:
            # Если из селектора пришли новые события, то обрабатываем их и убираем из обработки файловые дескрипторы.
            # Важный момент о хранении данных о задачах в селекторе: одна и та же задача может ожидать чтения данных и
            # пытаться записать новые данные. Именно поэтому в поле data хранится кортеж (reader, writer).
            fileobj, (reader, writer) = key.fileobj, key.data
            if mask & EVENT_READ and reader is not None:
                self.schedule(reader)
                self._remove_reader(fileobj)  # вот тут убираем дескриптовр
            if mask & EVENT_WRITE and writer is not None:
                self.schedule(writer)
                self._remove_writer(fileobj)

    # В рамках планировщика добавляем специальную бесконечную задачу io_task перед стартом цикла событий.
    def io_task(self) -> Generator:
        # У этой функции есть бесконечный цикл внутри, а также она передаёт управление планировщику
        while True:
            # Если очередь задач пустая, то timeout для ожидания событий из селектора ставится в режим «до тех пор,
            # пока не будет новых событий».
            if self.ready.empty():
                self.io_poll(None)
            # В остальных случаях ставим таймаут 0, чтобы получить все события от ОС сразу же, как они произойдут.
            else:
                self.io_poll(0)
            yield

