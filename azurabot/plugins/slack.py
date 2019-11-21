"""
The Slack interface plugin.
"""

from azurabot.interface.threadedinterface import ThreadedInterface


class Plugin(ThreadedInterface):

    async def start(self):
        self.name = "Slack"
        self.log("Started.")
