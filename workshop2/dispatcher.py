import logging
import time
from typing import List

from workshop2.task import Task

logger = logging.getLogger(__name__)

class Dispatcher:
    def __init__(self):
        self._queue: List[Task] = []

    def add_task(self, task: Task) -> None:
        self._queue.append(task)

    def _get_task(self) -> Task|None:
        if not self._queue:
            return None
        task = self._queue.pop(0)
        return task

    def _process_task(self, task: Task|None) -> None:
        if not task:
            return None
        try:
            result = task.run()
        except StopIteration:
            logger.info(f"Task {task.id} finished.")
            return None
        self.add_task(task)
        return result

    def run(self) -> None:
        while True:
            task = self._get_task()
            self._process_task(task)
            time.sleep(.1)
