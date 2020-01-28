"""
The async inteface class file.
"""

import configparser

import azurabot.interface.interface as interface


class AsyncInterface(interface.Interface):
    async def start(self, config: configparser.ConfigParser):
        self.config = config
        await self.run()

    async def run(self):
        self.log(f"Plugin {self.name} doesn't have its own run() function.")
