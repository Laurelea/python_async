class SingletonMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)

        return cls.instance


class SingletonBaseMeta(metaclass=SingletonMeta):
    pass


singleton1 = SingletonBaseMeta()
singleton2 = SingletonBaseMeta()

print(id(singleton1))
print(id(singleton2))
print(singleton1 == singleton2)

# При наследовании создаются разные объекты классов А и В

class A(SingletonBaseMeta):
    pass

class B(A):
    pass

print(A())
print(B())