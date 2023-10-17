'''
type — самая простая реализация метакласса. У полученных из неё классов — тип type. Каждый из них представляет собой класс, который выступает в качестве своего метакласса.
Опишем классы, которые наследуются от него. Их можно использовать как метаклассы.
'''


class MyMeta(type):
    def __new__(cls, cls_name, parents, attrs):
        print("my_meta: вызвали метод __new__")
        return super().__new__(cls, cls_name, parents, attrs)

    def __call__(self, *args, **kwargs):
        print("my_meta: вызвали метод __call__")
        return super().__call__(*args, **kwargs)


class MyClass(metaclass=MyMeta):
    pass

inst = MyClass()

#>> output
# MyMeta: вызвали метод __new__
# MyMeta: вызвали метод __call__