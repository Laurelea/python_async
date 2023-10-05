# одновременно и итерируемы объект, и итератор
class Range:
    def __init__(self, start: int, end: int, step: int = 1):
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self):  # часть итерируемого объекта
        self.current = self.start
        return self

    def __next__(self):  # часть итератора
        if self.current < self.end:
            value = self.current
            self.current += self.step
            return value

        raise StopIteration

range_ = Range(1, 9, 2)
for idx in range_:
    print(idx)
