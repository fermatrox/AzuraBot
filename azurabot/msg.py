"""
The msg class file.
"""

import asyncio

from azurabot.user import User
from azurabot.plugins.plugin import Plugin

# direction
TO_BOT = 1
FROM_BOT = 2


class Msg:
    """Represents a message between a user and the bot.

    direction: TO_BOT or FROM_BOT
    user: the User object representing the user.
    reply_to: the asyncio.Queue to send any reply to.
    text: the text of the message.

    Messages are sent either from a user, through an Interface to
    the bot, or the other way around (as indicated by "direction").

    When a plugin, say the IRC plugin, receives a message from the IRC
    server, it forwards it to the bot. When it does so, it creates a
    User object in which it fills out the data it has; in that case,
    the user's IRC nickname and perhaps something else. Then, when the
    message reaches the bot itself, the bot will (if it finds the user
    in the database), fill out the object with other fields it found
    in the database, such as perhaps the user's name on other
    services. That might be a security risk though, so I might not do
    that last part.

    """

    def __init__(self,
                 direction: int,
                 user: User,
                 reply_to: asyncio.Queue,
                 text: str=None):
        self.direction = direction
        self.user = user
        self.reply_to = reply_to
        self.text = text

    async def reply(self, text: str, replyer_inbox: asyncio.Queue):
        if self.direction == TO_BOT:
            direction = FROM_BOT
        else:
            direction = TO_BOT

        reply_msg = Msg(direction=direction,
                        user=self.user,
                        reply_to=replyer_inbox,
                        text=text)
        await self.reply_to.put(reply_msg)

    def __str__(self):
        if self.direction == TO_BOT:
            preposition = "from"
        elif self.direction == FROM_BOT:
            preposition = "to"

        if self.text:
            return f"Msg {preposition} {self.user.name}: {self.text}"
        else:
            return f"Empty Msg {preposition} {self.user.name}"
