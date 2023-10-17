import logging
from datetime import datetime, timedelta
from typing import Callable

from workshop2.sc import SleepCall

logger = logging.getLogger(__name__)

class Task:
    def __init__(self, id: int, target: Callable, *args, **kwargs):
        self.id = id
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._generator = self._target(*self._args, **self._kwargs)
        self.deffered_till = None

    def run(self):
        """Исполнить задачу"""

        if self.deffered_till and self.deffered_till > datetime.now():
            logger.info(f"Task {self.id} still not ready. Skip.")
            return

        result = next(self._generator)

        if isinstance(result, SleepCall):
            logger.info(f"Task {self.id} wanna sleep for {result.sec}")
            self.deffered_till = datetime.now() + timedelta(seconds=result.sec)

        return result