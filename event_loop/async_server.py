import logging
from socket import socket, AF_INET, SOCK_STREAM
from systemcall import NewTask
from scheduler import Scheduler
from async_socket import AsyncSocket

logger = logging.getLogger(__name__)


def handle_client(client, addr):
    print("Connection from", addr)
    while True:
        data = yield from client.recv(65536)
        if not data:
            break
        yield from client.send(data)
    print("Client closed")
    client.close()


def server(port):
    print("Server starting")
    rawsock = socket(AF_INET, SOCK_STREAM)
    rawsock.bind(("", port))
    rawsock.listen()
    sock = AsyncSocket(rawsock)
    try:
        while True:
            client, addr = yield from sock.accept()
            yield NewTask(handle_client(client, addr))
    finally:
        sock.close()


if __name__ == "__main__":
    shed = Scheduler()
    shed.add_task(server(8000))
    shed.event_loop()