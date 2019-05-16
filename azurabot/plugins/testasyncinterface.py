"""
A test plugin for the async interface.
"""

import asyncio

from azurabot.interface.asyncinterface import AsyncInterface


class Plugin(AsyncInterface):

    async def start(self):
        print("Async plugin started.")
        send_task = asyncio.create_task(self.send_msg("Hello, bot!"))
        await asyncio.gather(send_task)

    async def send_msg(self, payload: str):
        await asyncio.sleep(2)
        print("Sending...")
        await self.bot_inbox.put(payload)
