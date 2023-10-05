# пример с sentinel

class Sequence:

    items = [1, 3, 5, 7, 9]

    def __init__(self):
        self.index = 0

    def __call__(self, *args, **kwargs):
        value = self.items[self.index]
        self.index += 1
        return value


def for_loop(callable, sentinel=None):
    iterator = iter(callable, sentinel)
    has_next = True
    while has_next:
        try:
            item = next(iterator)
        except StopIteration:
            has_next = False
        else:
            print(item)


for_loop(Sequence(), 9)
