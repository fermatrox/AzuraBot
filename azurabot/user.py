"""
The user class file.
"""


class User:
    """
    Represents a user who communicates with the bot.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return "User: %s" % self.name
