from __future__ import annotations
from socket import socket
from typing import Tuple
from systemcall import SystemCall

# Wait for writing
# это пользовательское событие (SystemCall), которое представляет асинхронное ожидание возможности записи в файловый дескриптор f. Когда это событие обрабатывается, планировщик регистрирует задачу task для ожидания события записи на указанном файловом дескрипторе f.
class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self, sched, task):
        # определяет дескриптор файла открытого потока данных по указателю на управляющую таблицу потока данных
        fd = self.f.fileno()
        sched.wait_for_write(task, fd)

# Wait for reading
class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self, sched, task):
        fd = self.f.fileno()
        sched.wait_for_read(task, fd)

class AsyncSocket:
    def __init__(self, sock: socket):
        self.sock = sock

    # Здесь реализованы все четыре функции, которыми пользуется echo-сервер.
    def accept(self) -> Tuple['AsyncSocket', str]:
        # Чтобы сокет был доступен в любой момент, используются SystemCall функции WriteWait и ReadWait.
        yield ReadWait(self.sock)
        client, addr = self.sock.accept()
        return AsyncSocket(client), addr

    def send(self, buffer: bytes):
        # Блокировка работы обычно происходит из-за того, что сокет не готов обрабатывать ту или иную операцию.
        while buffer:
            yield WriteWait(self.sock)
            len = self.sock.send(buffer)
            buffer = buffer[len:]

    def recv(self, maxbytes: int) -> bytes:
        yield ReadWait(self.sock)
        return self.sock.recv(maxbytes)

    def close(self):
        yield self.sock.close()
