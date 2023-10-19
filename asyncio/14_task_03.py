"""
Задание 3
Создайте сервер на основе asyncio, который раз в 2 секунды отправляет подключённым клиентам текущий статус — время и
количество подключённых клиентов. Для реализации используйте метод create_server().
"""

"""
Работает частично
Посылает все как надо, но не отслеживает отсоединение клиента.
"""

import logging
import sys
import asyncio
from asyncio.streams import StreamReader, StreamWriter
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

CONNECTIONS = set()

def send_date(writer):
    if writer.is_closing():
        address = writer.get_extra_info('peername')
        logger.info('Stop serving %s', address)
        writer.close()
        CONNECTIONS.remove(address)
    else:
        data = f'{datetime.now().replace(microsecond=0)} connections: {len(CONNECTIONS)}\n'
        writer.write(data.encode())
        asyncio.get_running_loop().call_later(3, send_date, writer)


async def client_connected(reader: StreamReader, writer: StreamWriter):
    address = writer.get_extra_info('peername')
    CONNECTIONS.add(address)
    logger.info('Start serving %s', address)

    loop = asyncio.get_running_loop()

    while True:
        loop.call_later(3, send_date, writer)
        await asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True)


async def main(host: str, port: int):
    srv = await asyncio.start_server(client_connected, host, port)
    async with srv:
        await srv.serve_forever()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 8000))

