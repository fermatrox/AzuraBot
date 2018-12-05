#!/usr/bin/env python

"""
My own version of input_exp.py.
"""

import asyncio
import functools
import sys

class Prompt(object):

    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.q = asyncio.Queue(loop=self.loop)
        self.loop.add_reader(sys.stdin, self.got_input)

    def got_input(self):
        asyncio.ensure_future(self.q.put(sys.stdin.readline()),
                              loop=self.loop)

    async def __call__(self, msg, end="\n", flush=True):
        print(msg, end=end, flush=flush)
        return (await self.q.get()).rstrip("\n")

prompt = Prompt()
raw_input = functools.partial(prompt, end="", flush=True)

async def main():
    # await prompt("press enter to continue")

    while True:
        print(await raw_input("enter something:"))
            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
