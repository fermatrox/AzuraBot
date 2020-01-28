#!/usr/bin/env python3

import asyncio
import configparser
import os
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
        if not os.path.isfile("etc/azurabot.conf"):
            raise AzuraBotError("Config file etc/azurabot.conf not found")
        self.config.read("etc/azurabot.conf")

        self.plugins = []

    async def run(self):
        # user = azurabot.user.User("Enfors")
        # msg = azurabot.msg.Msg(azurabot.msg.FROM_USER, user, "foo")
        # print(user)
        # print(msg)
        self.bot_inbox = asyncio.Queue()

        #
        # Step 1: Load all plugins
        #
        await self._load_all_plugins()

        #
        # Step 2: Start all plugins
        #
        await self._start_all_plugins()

        #
        # Step 3: Start all background tasks
        #
        await self._start_cron_task()

        #
        # Step 4: Enter main loop
        #
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

        while keep_running:
            pass
            msg = await self.bot_inbox.get()
            text = msg.text
            print("[bot] Received text: '%s'" % text)

            # The reason why we start a task here, is because in the future, the functio
            # _handle_inc_msg() might be slow - perhaps it has to load users from a slow
            # database, or something. 
            asyncio.create_task(self._handle_inc_msg(msg))
            
            # if text == "Hello, bot!":
            #     print("[bot] Replying...")
            #     await msg.reply("Hello yourself!", self.bot_inbox)
            # else:
            #     print("[bot] Replying again...")
            #     await msg.reply("Your message has been received.",
            #                     self.bot_inbox)
            #     keep_running = False

    async def _start_all_plugins(self):

        start_tasks = []

        for plugin in self.plugins:
            start_tasks.append(asyncio.create_task(plugin.start(self.config)))

        await asyncio.gather(*start_tasks)

    async def _start_cron_task(self):
        """This function starts the background timer task. For example, if
        users want a weather report at a certain time each day, it
        will be handled by the background timer.

        """
        pass
        
    async def _handle_inc_msg(self, msg: azurabot.msg.Msg):

        user = await self._identify_msg_user(msg)
        
        msg = await self._filter_inc_msg(msg)

        intent = await self._select_intent(msg)

        out_msgs = await self._run_backend(intent)

        for out_msg in out_msgs:
            await self._handle_out_msg(out_msg)

    async def _identify_msg_user(self, msg: azurabot.msg.Msg):
        user = msg.user
        await user.identify()
        print(f"[bot] User identified: {user}")
        return user
            
    async def _filter_inc_msg(self, msg: azurabot.msg.Msg):
        return msg

    async def _select_intent(self, msg: azurabot.msg.Msg):
        return None

    async def _run_backend(self, intent):
        return []

    async def _handle_out_msg(self, msg: azurabot.msg.Msg):
        pass


class AzuraBotError(Exception):
    pass


if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.run())
