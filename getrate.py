# coding: utf-8

import asyncio
import json
from zmq.asyncio import Context
import zmq
from tornado.options import define, options
import random
import logging

define("port", default=8888, help="port to pub/sub")
define("debug", default=False, help="asyncio debug flg")

def async_debug(loop: asyncio.AbstractEventLoop):
    loop.set_debug(True)
    logging.basicConfig(level=logging.DEBUG)

async def recv(socket: zmq.Socket):
    while True:
        topic,data = await socket.recv_multipart()
        print(data)
        obj = json.loads(data)
        print(obj)

def main():
    loop = asyncio.get_event_loop()
    if(options.debug):
        async_debug(loop)
    context = Context.instance()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:%s" % options.port)
    socket.subscribe(b'')


    loop.run_until_complete(recv(socket))
    loop.close()

if __name__ == '__main__':
    options.parse_command_line()
    main()

