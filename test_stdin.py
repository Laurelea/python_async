import sys

print('Получим данные из stdin:')
# В консоли нужно напечатать какое-нибудь сообщение
s = input()
print('Выведем данные в stdout: ', s)
print('Выведем данные в stderr: ', s, file=sys.stderr)