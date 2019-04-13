"""
The msg class file.
"""

from azurabot.user import User

# msg_type
FROM_USER = 1
TO_USER = 2


class Msg:
    """
    Represents a message between a user and the bot.
    """

    def __init__(self,
                 msg_type: int,
                 user: User,
                 payload: str=None):
        self.msg_type = msg_type
        self.user = user
        self.payload = payload

    def __str__(self):
        if self.msg_type == FROM_USER:
            preposition = "from"
        elif self.msg_type == TO_USER:
            preposition = "to"

        if self.payload:
            return f"Msg {preposition} {self.user.name}: {self.payload}"
        else:
            return f"Empty Msg {preposition} {self.user.name}"
