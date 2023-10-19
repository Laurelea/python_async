"""
Реализация от наставника
"""

import asyncio
import time

clients = []

async def handle_client(reader, writer):
    clients.append(writer)
    try:
        while True:
            await asyncio.sleep(5)  # Ждем 5 секунд
            message = f"Количество подключенных клиентов: {len(clients)}, Время: {time.strftime('%H:%M:%S')}"
            for client_writer in clients:
                try:
                    client_writer.write(message.encode())
                    await client_writer.drain()
                except Exception as e:
                    print(f"Ошибка при отправке сообщения: {e}")
    except asyncio.CancelledError:
        pass
    finally:
        clients.remove(writer)
        writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

asyncio.run(main())