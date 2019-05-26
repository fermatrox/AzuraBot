"""
The Interface class file.

You won't normally use this directly, but rather one of its
decendants interface.async or interface.threaded.
"""

import asyncio

import azurabot


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

    async def send_msg_to_bot(self, msg: azurabot.msg.Msg):
        """
        Send any kind of message to the bot.
        """
        await self.bot_inbox.put(msg)

    async def send_user_text_to_bot(self, user: azurabot.user.User, text: str):
        """
        Send a text message from the user to the bot.
        """
        msg = azurabot.msg.Msg(direction=azurabot.msg.FROM_USER,
                               user=user,
                               reply_to=self.inbox,
                               payload=text)
        await self.send_msg_to_bot(msg)

    def start(self):
        pass
