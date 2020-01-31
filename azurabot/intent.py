"""
An "intent" is the intent of a user.

If a user says "What's the weather tomorrow in Karlstad," then the user's intent is
to get a weather forecast. This file is all about intents.
"""

import azurabot


class Intent:
    """This class represents the "intent" behind a user's command.
    """

    def __init__(self, bot):
        self.bot = bot
        self.name = None
        self.confidence = 0 # How confident we are that this is the right intent
        self.intent_file = "(unset - set it in the intent file)"
        
    async def do(self, user: azurabot.user.User, msg: azurabot.msg.Msg):
        pass
