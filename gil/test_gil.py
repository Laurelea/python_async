# python 3.9.5

import sys

# Переменная 'a' первая ссылается на объект object()
a = object()
# Переменная 'b' вторая ссылается на объект object()
b = a
# Так как вы передаёте переменную 'a', которая ссылается на объект,
# аргумент функции тоже будет ссылаться на этот объект
# В итоге на объект будет указывать три ссылки
print(sys.getrefcount(a))
