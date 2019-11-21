"""
The threaded interface class file.
"""

import asyncio
import threading

import azurabot.interface.interface as interface


class ThreadedInterface(interface.Interface):
    async def start(self):
        self.name = "(unnamed threaded interface plugin)"
        self.thread = threading.Thread(target=self.thread_start)
        self.thread.start()

    def thread_start(self):
        self.loop = asyncio.new_event_loop()
        await self.run()
