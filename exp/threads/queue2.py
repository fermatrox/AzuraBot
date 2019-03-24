#!/usr/bin/env python

"""
This example is similar to queue1.py, but it tries to send the
message from a different thread.
"""

import asyncio
import threading


async def recv_msg(q):
    msg = await q.get()
    # print(".", end="", flush=True)
    print("Received message:", msg)


async def send_msg(q, msg):
    # await asyncio.sleep(0.5)
    t = threading.Thread(target=prepare_msg,
                         args=(q, msg))
    t.start()
    t.join()
    print("Message sent.")


def prepare_msg(q, msg):
    loop = asyncio.new_event_loop()
    snd_task = loop.create_task(send_msg_from_thread(q, msg))
    loop.run_until_complete(snd_task)


async def send_msg_from_thread(q, msg):
    await q.put(msg)


async def main():
    # Create two tasks.
    q = asyncio.Queue()

    # for i in range(0, 1000):
    send_task = asyncio.create_task(send_msg(q, "Hello World"))
    recv_task = asyncio.create_task(recv_msg(q))

    await asyncio.gather(send_task, recv_task)


asyncio.run(main())
