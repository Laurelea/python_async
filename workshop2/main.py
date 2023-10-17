import logging
import sys
import time

from workshop2.dispatcher import Dispatcher
from workshop2.task import Task
from workshop2.sc import SleepCall

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


def do_something(task_name: str, sleep_second: float = 5.0):
    logger.info(f"{task_name} did something")
    yield SleepCall(sleep_second)
    logger.info(f"{task_name} did something again")


if __name__ == '__main__':
    dp = Dispatcher()
    for i in range(5):
        task = Task(
            id=i,
            target=do_something,
            task_name=f"Task {i}",
            sleep_second=5,
        )
        dp.add_task(task)
    dp.run()
