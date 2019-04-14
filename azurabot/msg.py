"""
The msg class file.
"""

from azurabot.user import User

# direction
FROM_USER = 1
TO_USER = 2


class Msg:
    """
    Represents a message between a user and the bot.
    """

    def __init__(self,
                 direction: int,
                 user: User,
                 payload: str=None):
        self.direction = direction
        self.user = user
        self.payload = payload

    def __str__(self):
        if self.direction == FROM_USER:
            preposition = "from"
        elif self.direction == TO_USER:
            preposition = "to"

        if self.payload:
            return f"Msg {preposition} {self.user.name}: {self.payload}"
        else:
            return f"Empty Msg {preposition} {self.user.name}"
