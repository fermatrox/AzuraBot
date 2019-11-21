"""
The async inteface class file.
"""

import azurabot.interface.interface as interface


class AsyncInterface(interface.Interface):
    async def start(self):
        self.name = "(unnamed async interface plugin)"
        await self.run()

    async def run(self):
        self.log("This plugin doesn't have its own run() function.")
