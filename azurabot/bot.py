#!/usr/bin/env python3

import os
import re
import importlib

"""
AzuraBot's most important file.
"""


class Bot:
    def run(self):
        self._load_all_plugins()
        self._main_loop()

    def _load_all_plugins(self):
        reg = re.compile("f.*\.py$", re.IGNORECASE)
        file_names = filter(reg.search,
                            os.listdir(os.path.join(os.path.dirname(__file__),
                                                    "plugins")))
        for file_name in file_names:
            self._load_plugin(file_name[:-3])

    def _load_plugin(self, file_name):
        print("Loading plugin", file_name)

        file = importlib.import_module("plugins." + file_name)
        plugin = file.Plugin()
        plugin.start()

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


if __name__ == "__main__":
    bot = Bot()
    bot.run()
