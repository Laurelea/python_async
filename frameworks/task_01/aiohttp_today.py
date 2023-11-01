import aiohttp
from aiohttp import web
from datetime import datetime

async def get_date():
    date = datetime.today().strftime('%H часов %M минут %m.%d.%Y года')
    # result = await response.json(content_type='text/html; charset=utf-8')
    # return result.get('text')
    return date
#
async def date_handler(request):
    # Формируем ответ для клиента
    return web.Response(text=await get_date())


async def make_app():
    app = web.Application()

    # Добавим необходимый URL
    app.add_routes([web.get('/today', date_handler)])
    return app


web.run_app(make_app())  # Запускаем приложение