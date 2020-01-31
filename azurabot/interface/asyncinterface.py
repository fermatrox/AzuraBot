"""
The async inteface class file.
"""

import configparser

import azurabot.interface.interface as interface


class AsyncInterface(interface.Interface):
    async def start(self):
        await self.run()
