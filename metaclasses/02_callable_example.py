'''
Метаклассы можно применять к классу. Для этого требуется вызываемый объект — callable,
который принимает указанные три параметра и возвращает объект класса.
'''


def metaclass_creator(class_name, parents, attrs):
    return "Simple metaclass"


class MyClass(metaclass=metaclass_creator):
    pass

print(MyClass)
print(type(MyClass))

# >> output
# Simple metaclass
# <class 'str'>