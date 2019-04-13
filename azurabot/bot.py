#!/usr/bin/env python3

import configparser
import importlib
import os

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

    def run(self):
        user = azurabot.user.User("Enfors")
        msg = azurabot.msg.Msg(azurabot.msg.FROM_USER, user, "foo")
        print(user)
        print(msg)
        self._load_all_plugins()
        self._main_loop()

    def _load_all_plugins(self):
        """
        Load all plugins.
        """
        plugins_dir = self.config["plugins"]["dir"]
        plugins_str = self.config["plugins"]["plugins"].replace("\r", "")
        file_names = [file_name for file_name in plugins_str.split("\n")
                      if len(file_name)]
        for file_name in file_names:
            self._load_plugin(f"{plugins_dir}.{file_name}")

    def _load_plugin(self, file_name):
        """
        Load a single plugin. Return True on success.
        """
        if file_name.endswith(".py"):
            file_name = file_name[:-3]

        print("Loading plugin", file_name)

        try:
            file = importlib.import_module(file_name)
        except ModuleNotFoundError:
            print("Plugin not found:", file_name.replace(".", "/") + ".py")
            return False
        plugin = file.Plugin()
        plugin.start()
        return True

    def _main_loop(self):
        pass

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
    bot.run()
