import asyncio
from datetime import datetime

ONLINE_CLIENTS = []


class EchoProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        ONLINE_CLIENTS.append(self.transport)

    def data_received(self, data):
        self.transport.write(data)

    def connection_lost(self, exc):
        print("Connection closed")
        self.transport.close()
        ONLINE_CLIENTS.remove(self.transport)


async def send_time():
    while True:
        for transport in ONLINE_CLIENTS:
            transport.write(
                (
                        datetime.now().strftime("%Y/%m/%d %H:%M:%S") +
                        f'. Connected {len(ONLINE_CLIENTS)}\n'
                ).encode()
            )
        await asyncio.sleep(3)


async def main(host: str, port: int):
    loop = asyncio.get_running_loop()
    loop.create_task(send_time())
    server = await loop.create_server(EchoProtocol, host, port)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 8000))