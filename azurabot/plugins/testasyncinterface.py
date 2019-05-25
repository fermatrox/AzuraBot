"""
A test plugin for the async interface.
"""

import asyncio

import azurabot

from azurabot.interface.asyncinterface import AsyncInterface


class Plugin(AsyncInterface):

    async def start(self):
        print("Async plugin started.")
        send_task = asyncio.create_task(self.send_msg("Hello, bot!"))
        await asyncio.gather(send_task)

    async def send_msg(self, payload: str):
        await asyncio.sleep(2)

        user = azurabot.user.User(identifiers={"testinterface": "Tester"})
        msg = azurabot.msg.Msg(direction=azurabot.msg.FROM_USER,
                               user=user,
                               reply_to=None,
                               payload="Hello, bot!")

        print("Sending...")
        await self.bot_inbox.put(msg)
