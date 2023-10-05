from typing import Iterable


class CyclicIterator:
    def __init__(self, iterable: Iterable):
        self.iterable = iterable
        self.my_iterator = iter(self.iterable)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            value = next(self.my_iterator)
        except StopIteration:
            self.my_iterator = iter(self.iterable)
            value = next(self.my_iterator)
        return value

if __name__ == '__main__':
    a = [3, 7, 9, 10]
    b = (4, 5, 7)
    c = {5, 6, 7, 9}
    d = range(5)

    cyclic_iterator = CyclicIterator(d)
    for i in cyclic_iterator:
        print(i)
