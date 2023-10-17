import logging
import sys
import asyncio
from asyncio.streams import StreamReader, StreamWriter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


# Для каждого нового соединения вызывается функция client_connected, которой передаются два стрима на вход:
# StreamReader и StreamWriter
# Функции очень похожи на те, которые используются в сокетах (recv → read).
async def client_connected(reader: StreamReader, writer: StreamWriter):
    address = writer.get_extra_info('peername')
    logger.info('Start serving %s', address)

    while True:
        # Через StreamReader нужно получать данные от клиента.
        data = await reader.read(1024)
        if not data:
            break

        # Для передачи данных обратно клиенту используется StreamWriter, который работает чуть хитрее, чем сокет.
        # Для записи данных в стрим используется функция write, которая записывает данные в специальный буфер.
        writer.write(data)
        # Чтобы отправить данные клиенту из буфера, необходимо вызвать асинхронную функцию drain.
        await writer.drain()

    logger.info('Stop serving %s', address)
    # После обработки соединения стрим на отдачу данных клиентов необходимо закрыть через функцию close.
    writer.close()


async def main(host: str, port: int):
    # Для работы с новыми подключениями у asyncio есть функция start_server, которая отдаёт объект Server

    srv = await asyncio.start_server(client_connected, host, port)

    # С помощью него можно запустить вечную обработку новых и существующих соединений через функцию serve_forever.
    async with srv:
        await srv.serve_forever()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 8000))
