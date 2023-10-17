'''
Другой пример использования — шаблоны проектирования, например, Singleton.
Он ограничивает создание экземпляров класса только одним объектом.
'''


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MySingleton(metaclass=SingletonMeta):
    pass


singleton1 = MySingleton()
singleton2 = MySingleton()

print(id(singleton1))
print(id(singleton2))
print(singleton1 == singleton2)

# >> output
# 140517583372784
# 140517583372784
# True