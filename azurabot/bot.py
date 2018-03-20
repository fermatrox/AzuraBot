#!/usr/bin/env python3

"""
AzuraBot's most important file.
"""


class Bot:
    def run(self):
        self._load_all_plugins()
        self._main_loop()

    def _load_all_plugins(self):
        pass

    def _load_plugin(self, file_name):
        pass

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
