"""
The base Plugin class file.

All other plugins inherit this class, directly or indirectly.
"""

import asyncio
import configparser

class Plugin:

    def __init__(self, config: configparser.ConfigParser, bot_inbox: asyncio.Queue,
                 name="(unnamed plugin)"):
        self.config = config
        self.bot_inbox = bot_inbox
        self.name = name

    async def start(self):
        """
        When a plugin is loaded by the bot, the bot calls its
        start() function. That function is then responsible for
        calling the object's run() function.

        This is done by AsyncInterface's and ThreadedInterface's
        start() function, which typically should not be overridden.
        """
        #self.log("This plugin doesn't have its own start() function.")
        pass

    async def run(self):
        """
        Called by the plugin's start() function. Ordinary plugins
        should put their code here.
        """
        self.log("This plugin doesn't have its onw run() function.")

    def log(self, msg):
        print(f"[{self.name}] {msg}")
