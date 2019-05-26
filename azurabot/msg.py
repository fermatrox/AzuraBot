"""
The msg class file.
"""

import asyncio

from azurabot.user import User

# direction
FROM_USER = 1
TO_USER = 2


class Msg:
    """
    Represents a message between a user and the bot.

    direction: FROM_USER or TO_USER
    user: the User object representing the user.
    reply_to: the asyncio.Queue to send any reply to.
    payload: the contents of the message.

    Messages are sent either from a user, through an Interface to
    the bot, or the other way around (as indicated by "direction").
    """

    def __init__(self,
                 direction: int,
                 user: User,
                 reply_to: asyncio.Queue,
                 payload: str=None):
        self.direction = direction
        self.user = user
        self.reply_to = reply_to
        self.payload = payload

    async def reply(self, payload: str, replyer_inbox: asyncio.Queue):
        if self.direction == FROM_USER:
            direction = TO_USER
        else:
            direction = FROM_USER

        reply_msg = Msg(direction=direction,
                        user=self.user,
                        reply_to=replyer_inbox,
                        payload=payload)
        await self.reply_to.put(reply_msg)

    def __str__(self):
        if self.direction == FROM_USER:
            preposition = "from"
        elif self.direction == TO_USER:
            preposition = "to"

        if self.payload:
            return f"Msg {preposition} {self.user.name}: {self.payload}"
        else:
            return f"Empty Msg {preposition} {self.user.name}"
