"""
This file contains a set of standard intents, which should always be included.
"""

import azurabot
from azurabot.intent import Intent
from azurabot.interface.asyncinterface import AsyncInterface
from azurabot.msg import Msg


class HelloIntent(Intent):
    name = "Hello"
    
    def __init__(self, bot: azurabot.bot.Bot):
        super().__init__(bot)
        self.intent_file = __file__
    
    async def do(self, user: azurabot.user.User, msg: Msg):
        await msg.reply(f"Hello {user.name}!", user.inbox)

        
class Plugin(azurabot.plugins.plugin.Plugin):
    name = "std_intents"
    # By setting "intents", we signal to the bot that there are intents to use here.    
    intents = [ HelloIntent ]

    async def run(self):
        pass

