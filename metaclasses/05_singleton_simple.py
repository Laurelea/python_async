class SingletonBase:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)

        return cls.instance

singleton1 = SingletonBase()
singleton2 = SingletonBase()

print(id(singleton1))
print(id(singleton2))
print(singleton1 == singleton2)

# При создании класса B возвращается тот же инстанс, то есть класс А, в этом косяк метода

class A(SingletonBase):
    pass

class B(A):
    pass

print(A())
print(B())