"""
Sample plugin.
"""

import asyncio


class Plugin:
    def __init__(self, bot_inbox: asyncio.Queue):
        self.bot_inbox = bot_inbox

    def start(self):
        print("Plugin started.")
