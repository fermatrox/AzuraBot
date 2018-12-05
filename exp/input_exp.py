#!/usr/bin/env python

"""
Based on an answer to
https://stackoverflow.com/questions/35223896/listen-to-keypress-with-asyncio,
by bj0.
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
    await prompt("press enter to continue")

    print(await raw_input("enter something:"))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
