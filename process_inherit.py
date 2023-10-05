from multiprocessing import Process
from time import sleep


class CustomProcess(Process):
    def __init__(self, limit, **kwargs):
        super().__init__(**kwargs)
        self._limit = limit

    def run(self):
        for i in range(self._limit):
            print(f'Из CustomProcess: {i}')
            sleep(1)


if __name__ == "__main__":
    custom = CustomProcess(3, name='custom_name')
    custom.start()
    # custom.join()
    print('end')
