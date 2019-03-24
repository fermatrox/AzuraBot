#!/usr/bin/env python

"""
This example just tries to send a message from one task to another,
using a simple queue.

The next example (queue2.py) will try to do the same, but send it
from a different thread.
"""

import asyncio


async def recv_msg(q):
    msg = await q.get()
    print("Received message:", msg)

async def send_msg(q, msg):
    await asyncio.sleep(2)
    await q.put(msg)
    print("Message sent.")

async def main():
    # Create two tasks.
    q = asyncio.Queue()
    send_task = asyncio.create_task(send_msg(q, "Hello World"))
    recv_task = asyncio.create_task(recv_msg(q))

    await asyncio.gather(send_task, recv_task)

asyncio.run(main())
