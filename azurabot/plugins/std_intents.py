"""
This file contains a set of standard intents, which should always be included.
"""

import azurabot
from azurabot.intent import Intent
from azurabot.interface.asyncinterface import AsyncInterface
from azurabot.msg import Msg


class HelloIntent(Intent):

    def __init__(self):
        super().__init__()
        self.name = "Hello"
        self.intent_file = __file__
    
    async def do(self, user: azurabot.user.User, msg: Msg, data: dict=None):
        await msg.reply(f"Hello {user.name}!", user.inbox)

        
class Plugin(AsyncInterface):
    # By setting "intents", we signal to the bot that there are intents to use here.
    intents = [ HelloIntent() ]

    async def run(self):
        pass

