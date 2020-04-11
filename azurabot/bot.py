#!/usr/bin/env python3

import asyncio
import configparser
import os
import importlib

import azurabot.user
import azurabot.msg

from azurabot.intent import Intent
from azurabot.msg import Msg
from azurabot.user import User

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

        self.intents = {}

        self.online_users = {}

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

    async def reply(self, old_msg: Msg, text: str):
        """Given a previous message old_msg, this function replies to it with
        the text in the text argument.

        """
        if old_msg.direction == azurabot.msg.TO_BOT:
            direction = azurabot.msg.FROM_BOT
        else:
            direction = azurabot.msg.TO_BOT

        reply_msg = Msg(direction=direction,
                        user=old_msg.user,
                        reply_to=new_msg.reply_to,
                        text=text)
        await old_msg.put(reply_msg)
            
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

        base_name = file_name.split(".")[-1]

        print("[bot] Loading plugin", base_name)

        try:
            plugin_file = importlib.import_module(file_name)
        except ModuleNotFoundError:
            print("Plugin not found:", file_name.replace(".", "/") + ".py")
            return False
        plugin = plugin_file.Plugin(config=self.config,
                                    bot_inbox=self.bot_inbox,
                                    name=base_name)
        return plugin

    async def _main_loop(self):
        keep_running = True

        while keep_running:
            pass
            msg = await self.bot_inbox.get()
            text = msg.text
            print("[bot] Received text: '%s'" % text)

            # The reason why we start a task here, is because in the
            # future, the functio _handle_inc_msg() might be slow -
            # perhaps it has to load users from a slow database, or
            # something.

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
            print(f"[bot] Starting plugin {plugin.name}...")
            start_tasks.append(asyncio.create_task(plugin.start()))

            try:
                plugin_intents = plugin.intents

                await self._add_intents(plugin_intents)
            except AttributeError:
                pass

        await asyncio.gather(*start_tasks)

    async def _add_intents(self, intents: list):
        for intent in intents:
            await self._add_intent(intent)

    async def _add_intent(self, intent: Intent):
        if intent.name in self.intents:
            existing_intent = self.intents[intent.name]
            print(f"[bot] Intent conflict: {intent.name} exists in both "
                  f"{intent.intent_file} and {existing_intent.intent_file}. "
                  f"Using the one in {existing_intent.intent_file}.")
            return False

        print(f"[bot] Adding intent {intent.name}.")
        self.intents[intent.name] = intent

    async def _start_cron_task(self):
        """This function starts the background timer task. For example, if
        users want a weather report at a certain time each day, it
        will be handled by the background timer.

        """
        pass

    async def _handle_inc_msg(self, msg: azurabot.msg.Msg):

        user = await self._identify_msg_user(msg)

        if user.current_address not in self.online_users:
            self.online_users[user.current_address] = user
            user.loop_task = asyncio.create_task(self._user_loop(user))
            # asyncio.gather(user.loop_task) # todo: Maybe shouldn't be here
        else:
            user = self.online_users[user.current_address]

        # print(f"Putting message in user box {user.inbox!r}")
        await user.inbox.put(msg)

    async def _user_loop(self, user: azurabot.user.User):
        keep_running = True
        # out_msgs = []

        print(f"[bot] User loop started for {user.current_address}")

        while keep_running:
            # print(f"[bot] Awaiting messages from user box {user.inbox!r}")
            msg = await user.inbox.get()
            # print("[bot] Filtering")
            msg = await self._filter_inc_msg(msg)
            # print("[bot] Selecting intent")
            intent = await self._select_intent(msg)
            # print("[bot] Checking intent")
            if intent:
                await self._run_intent(user, intent, msg)
                print("[bot] Intent completed.")
            else:
                print("[bot] Intent failed.")
                await msg.reply("I'm sorry, but I don't understand.",
                                self.bot_inbox)

    async def _identify_msg_user(self, msg: azurabot.msg.Msg):
        user = msg.user
        await user.identify()
        print(f"[bot] User identified: {user}")
        return user

    async def _filter_inc_msg(self, msg: azurabot.msg.Msg):
        return msg

    async def _select_intent(self, msg: azurabot.msg.Msg):
        text = msg.text
        intent_name = text.split(" ")[0]
        try:
            intent = self.intents[intent_name](self)
            print(f"[bot] Intent: \"{intent_name}\"")
            return intent
        except KeyError:
            print(f"[bot] No intent found for \"{intent_name}\"")
            return None

    async def _run_intent(self, user: User, intent: Intent,
                          msg: azurabot.msg.Msg):
        await intent.do(user, msg)


class AzuraBotError(Exception):
    pass


if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.run())
