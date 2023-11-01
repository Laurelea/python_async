from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.server import Site

"""
Reactor. Это собственная реализация event-loop в Twisted — сердце любого Twisted-приложения. Объект реактора не
создаётся явно, а просто импортируется из библиотеки. После вызова reactor.run() он будет отвечать за весь цикл событий
в потоке:
появилось новое соединение и нужно задействовать фабрику для создания нового объекта протокола;
на соединение в протоколе поступили данные;
наступило время, на которое было назначено выполнение отложенной функции;
соединение разорвалось, поэтому информация о событии передаётся в соответствующий протокол.
"""


class Greeting(Resource):
    isLeaf = True

    def render_GET(self, request):
        return b"<html>Hello, world!</html>"


root = Resource()
root.putChild(b"hello", Greeting())
reactor.listenTCP(8080, Site(root))
reactor.run()

