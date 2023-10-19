"""
Задание 4
Доработайте решение, чтобы после 5 секунд неактивности клиент получал предупреждающее сообщение, а после 10 секунд
неактивности сервер автоматически разрывал соединение с клиентом.
"""

import asyncio
from datetime import datetime

ONLINE_CLIENTS = {}


class EchoProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        ONLINE_CLIENTS[self.transport] = datetime.now()

    def data_received(self, data):
        self.transport.write(data)
        ONLINE_CLIENTS[self.transport] = datetime.now()

    def connection_lost(self, exc):
        print("Connection closed")
        self.transport.close()
        del ONLINE_CLIENTS[self.transport]


async def send_time():
    while True:
        for transport in ONLINE_CLIENTS:
            transport.write(
                (
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                        f'. Connected {len(ONLINE_CLIENTS)}\n'
                ).encode()
            )
        await asyncio.sleep(3)


async def manage_timings():
    while True:
        for transport, last_activity in list(ONLINE_CLIENTS.items()):
            activity_absent = (datetime.now() - last_activity).seconds
            if activity_absent == 5:
                transport.write(f'No activity during last {activity_absent} secs...\n'.encode())
            elif activity_absent == 10:
                transport.write(f'No activity more than 10 secs, closing...\n'.encode())
                transport.close()
        await asyncio.sleep(1)


async def main(host: str, port: int):
    loop = asyncio.get_running_loop()
    loop.create_task(send_time())
    loop.create_task(manage_timings())
    server = await loop.create_server(EchoProtocol, host, port)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 8000))
