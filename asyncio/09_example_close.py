import asyncio

async def delay(delay):
    await asyncio.sleep(delay)

loop = asyncio.get_event_loop()
task1 = loop.create_task(delay(1))
task2 = loop.create_task(delay(2))
loop.run_until_complete(task1)  # запускаем только одну задачу
# если сейчас вызвать close() то будет ошибка Task was destroyed but it is pending!
# Чтобы такого не было:

# Закрываем незавершённые задачи
pending_tasks = asyncio.all_tasks(loop)
tasks = asyncio.gather(*pending_tasks, return_exceptions=True)
loop.run_until_complete(tasks)
loop.close()
