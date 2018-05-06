# coding: utf-8
from tornado import ioloop
from tornado import web
from tornado import websocket
from tornado.options import define, options
import logging
import asyncio
from zmq.asyncio import Context
import zmq
import json

def async_debug(loop: asyncio.AbstractEventLoop):
    loop.set_debug(True)
    logging.basicConfig(level=logging.DEBUG)

# command line options
define("port", default=8080, help="run on the given port")
define("zport", default=8888, help="zmq pubsub port")
define("debug", default=False, help="asyncio debug")

class RateWSHandler(websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        RateWSHandler.waiters.add(self)
    
    def on_close(self):
        RateWSHandler.waiters.remove(self)

    @classmethod
    def send_rate(cls,rate):
        for waiter in cls.waiters:
            try:
                waiter.write_message(rate)
            except:
                logging.error("Error sending message", exc_info=True)


async def recv(socket: zmq.Socket):
    print("subscribe socket")
    while True:
        topic,data = await socket.recv_multipart()
        print(topic,data)
        obj = json.loads(data)
        RateWSHandler.send_rate(obj)

app = web.Application([
    (r"/websocket", RateWSHandler),
    (r"/(.*)", web.StaticFileHandler, {"path": "./static", "default_filename": "index.html"})
],debug=True)

async def main():
    options.parse_command_line()
    if(options.debug):
        async_debug(asyncio.get_event_loop())

    context = Context.instance()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:%s" % options.zport)
    socket.subscribe(b'')
    app.listen(options.port)
    await recv(socket)

if __name__ == '__main__':
    ioloop.IOLoop.current().run_sync(main)
