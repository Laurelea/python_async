"""
Задание 3
Создайте сервер на основе asyncio, который раз в 2 секунды отправляет подключённым клиентам текущий статус — время и
количество подключённых клиентов. Для реализации используйте метод create_server().
"""

import logging
import sys
import asyncio
from asyncio.streams import StreamReader, StreamWriter
from datetime import datetime
import functools

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

CONNECTIONS = set()


def send_date(writer):
    data = f'{datetime.now().replace(microsecond=0)} connections: {len(CONNECTIONS)}\n'

    writer.write(data.encode())

    asyncio.get_running_loop().call_later(3, send_date, writer)
    # await writer.drain()



async def client_connected(reader: StreamReader, writer: StreamWriter):
    address = writer.get_extra_info('peername')
    CONNECTIONS.add(address)
    logger.info('Start serving %s', address)

    loop = asyncio.get_running_loop()
    # loop.call_later(3, functools.partial(send_date, writer))
    # loop.call_later(3, send_date, writer)
    # await writer.drain()

    while True:
        if writer.transport._conn_lost:
            logger.info(f'Connection lost: {address}')
            writer.close()
            CONNECTIONS.remove(address)
            await asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True)
            loop.close()
            break
        loop.call_later(3, send_date, writer)
        await writer.drain()
        try:
            loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True))
            # loop.run_forever()
        except asyncio.CancelledError as error:
            print(f'Cancelled error!!! {error}')
            exit(1)
        except ConnectionError:  # And/or whatever other exceptions you see.
            logger.info('Stop serving %s', address)
            writer.close()
            CONNECTIONS.remove(address)
            await asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True)
            break
        finally:
            loop.close()


    # while True:
    #     if writer.transport._conn_lost:
    #         logger.info(f'Connection lost: {address}')
    #         writer.close()
    #         CONNECTIONS.remove(address)
    #         await asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True)
    #         loop.close()
    #         break
    #
    #     try:
    #         await send_date(writer)
    #     except ConnectionResetError:  # And/or whatever other exceptions you see.
    #         logger.info('Stop serving %s', address)
    #         writer.close()
    #         CONNECTIONS.remove(address)
    #         await asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True)
    #         loop.close()
    #         break
    #     except BrokenPipeError:  # And/or whatever other exceptions you see.
    #         logger.info('Stop serving %s', address)
    #         writer.close()
    #         CONNECTIONS.remove(address)
    #         await asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True)
    #         loop.close()
    #         break


async def main(host: str, port: int):
    # Для работы с новыми подключениями у asyncio есть функция start_server, которая отдаёт объект Server

    srv = await asyncio.start_server(client_connected, host, port)

    # С помощью него можно запустить вечную обработку новых и существующих соединений через функцию serve_forever.
    async with srv:
        await srv.serve_forever()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 8000))

