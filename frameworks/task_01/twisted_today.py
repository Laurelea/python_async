from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.server import Site

from datetime import datetime

"""
Дополнительное задание
Чтобы лучше понять разницу в фреймворках, выполните следующее простое задание: на фреймворках Twisted и на aiohttp 
реализуйте сервис, который на GET-запрос на эндпоинт \today вернет сегодняшнюю дату и день недели.
"""

class Greeting(Resource):
    isLeaf = True

    def render_GET(self, request):
        return b"<html>Hello, world!</html>"


class Today(Resource):
    isLeaf = True

    def render_GET(self, request):
        date = datetime.today().strftime('%H часов %M минут %m.%d.%Y года')
        result = f'<html>{date}</html>'
        return bytes(result, 'utf-8')


root = Resource()
root.putChild(b"hello", Greeting())
root.putChild(b"today", Today())
reactor.listenTCP(8081, Site(root))
reactor.run()

