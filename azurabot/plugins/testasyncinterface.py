"""
A test plugin for the async interface.
"""

import asyncio

import azurabot

from azurabot.interface.asyncinterface import AsyncInterface


class Plugin(AsyncInterface):

    async def start(self):
        print("[plugin] Async plugin started.")
        send_task = asyncio.create_task(self.send_msg("Hello, bot!"))

    async def send_msg(self, payload: str):
        await asyncio.sleep(1)

        user = azurabot.user.User(identifiers={"testinterface": "Tester"})

        print("[plugin] Sending...")
        await self.send_user_text_to_bot(user, "Hello, bot!")
        answer = await self.inbox.get()
        print(f"[plugin] Received answer: '{answer.payload}'")

        await asyncio.sleep(1)

        print("[plugin] Sending...")
        await self.send_user_text_to_bot(user, "Nice to meet you!")
        answer = await self.inbox.get()
        print(f"[plugin] Received another answer: '{answer.payload}'")
