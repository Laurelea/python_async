'''
Класс — это объект с типом type, его можно считать самым простым метаклассом. Когда type получает на вход один параметр, то возвращает тип объекта, переданного в аргументах. Но при альтернативном вызове с тремя параметрами, он работает как метакласс и создаёт класс на основе переданных параметров:
имени класса;
родителей — классов, от которых происходит наследование;
атрибутов класса в виде словаря.

type — это метакласс, который язык использует для создания объекта. (поэтому у каждого объекта есть тип)
А поскольку type — это метакласс, мы можем создавать из него другие классы.
'''

MyClass = type('MyClass', (object,), {'test_attr': 15})
print(type(MyClass))

my_class_inst = MyClass()
print(my_class_inst.test_attr)

# >> output
# <class 'type'>
# 15