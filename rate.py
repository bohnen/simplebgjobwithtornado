# coding: utf-8

import asyncio
import json
import zmq
from tornado.options import define, options
import random
import logging

define("port", default=8888, help="port to pub/sub")
define("debug", default=False, help="asyncio debug flg")

async def get_rate(rate: float):
    return rate + random.uniform(-1,1)

def async_debug(loop: asyncio.AbstractEventLoop):
    loop.set_debug(True)
    logging.basicConfig(level=logging.DEBUG)

async def periodic_send(socket: zmq.Socket):
    rate = 100.0
    while True:
        bid = await get_rate(rate)
        ask = await get_rate(rate)
        if bid > ask:
            tmp = bid
            bid = ask
            ask = tmp
        rateobj = {"ask": ask,"bid":bid}
        print(rateobj)
        socket.send_multipart([b"TEST",json.dumps(rateobj).encode('utf-8')])
        await asyncio.sleep(1.0)

def main():
    loop = asyncio.get_event_loop()
    if(options.debug):
        async_debug(loop)
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % options.port)

    loop.run_until_complete(periodic_send(socket))
    loop.close()

if __name__ == '__main__':
    options.parse_command_line()
    main()

