"""
The Slack interface plugin.
"""

import configparser

from azurabot.interface.threadedinterface import ThreadedInterface


class Plugin(ThreadedInterface):

    async def start(self, config: configparser.ConfigParser):
        self.config = config
        self.name = "Slack"
        self.log("Started.")
