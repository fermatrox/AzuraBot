#!/usr/bin/env python3

import asyncio
import configparser
import importlib

import azurabot.user
import azurabot.msg

"""
AzuraBot's most important file.
"""


class Bot:
    """
    The bot itself. When you make a bot, it should inherit this class.
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("etc/azurabot.conf")

        self.plugins = []

    async def run(self):
        # user = azurabot.user.User("Enfors")
        # msg = azurabot.msg.Msg(azurabot.msg.FROM_USER, user, "foo")
        # print(user)
        # print(msg)
        self.bot_inbox = asyncio.Queue()
        await self._load_all_plugins()
        await self._main_loop()

    async def _load_all_plugins(self):
        """
        Load all plugins.
        """
        plugins_dir = self.config["plugins"]["dir"]
        plugins_str = self.config["plugins"]["plugins"].replace("\r", "")
        file_names = [file_name for file_name in plugins_str.split("\n")
                      if len(file_name)]
        for file_name in file_names:
            full_path = "%s.%s" % (plugins_dir, file_name)
            plugin = self._load_plugin(full_path)

            if plugin:
                self.plugins.append(plugin)

    def _load_plugin(self, file_name):
        """
        Load a single plugin. Return True on success.
        """
        if file_name.endswith(".py"):
            file_name = file_name[:-3]

        print("[bot] Loading plugin", file_name)

        try:
            file = importlib.import_module(file_name)
        except ModuleNotFoundError:
            print("Plugin not found:", file_name.replace(".", "/") + ".py")
            return False
        plugin = file.Plugin(self.bot_inbox)
        return plugin

    async def _main_loop(self):
        keep_running = True
        await self._start_all_plugins()
        while keep_running:
            msg = await self.bot_inbox.get()
            payload = msg.payload
            print("[bot] Received payload: '%s'" % payload)
            if payload == "Hello, bot!":
                print("[bot] Replying...")
                await msg.reply("Hello yourself!", self.bot_inbox)
            else:
                print("[bot] Replying again...")
                await msg.reply("Your message has been received.",
                                self.bot_inbox)
                keep_running = False

    async def _start_all_plugins(self):

        start_tasks = []

        for plugin in self.plugins:
            start_tasks.append(asyncio.create_task(plugin.start(self.config)))

        await asyncio.gather(*start_tasks)

    def _handle_inc_msg(self, msg):
        msg = self._filter_inc_msg(msg)

        intent = self._select_intent(msg)

        out_msgs = self._run_backend(intent)

        for out_msg in out_msgs:
            self._handle_out_msg(out_msg)

    def _filter_inc_msg(self, msg):
        return msg

    def _select_intent(msg):
        pass

    def _run_backend(self, intent):
        pass

    def _handle_out_msg(self, msg):
        pass


class AzuraBotError(Exception):
    pass


if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.run())
