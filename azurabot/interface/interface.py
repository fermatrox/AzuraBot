"""
The Interface class file.

You won't normally use this directly, but rather one of its
decendants interface.async or interface.threaded.
"""

import asyncio


class Interface:
    """
    Represents an interface between the bot and an external service,
    such as Slack or IRC. Basically, an interface talks to something
    in the external world, to which users connect.
    """

    def __init__(self, bot_inbox):
        self.bot_inbox = bot_inbox
        self.inbox = asyncio.Queue()

    async def put_msg(self, msg):
        await self.inbox.put(msg)

    async def get_msg(self):
        return await self.inbox.get()

    def start(self):
        pass
