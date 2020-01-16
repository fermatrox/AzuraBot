"""
An IRC interface plugin for AzuraBot.
"""

import asyncio
import configparser

import botymcbotface.async_irc

import azurabot

from azurabot.interface.asyncinterface import AsyncInterface


class Plugin(AsyncInterface):

    def __init__(self, config: configparser.ConfigParser):
        super().__init__(config)
        self.name = "irc"
    
    async def run(self):
        """This starts the plugin.
        """
        self.log("IRC plugin started.")
        await self._init_irc()
        asyncio.create_task(self._receive_loop())
        asyncio.create_task(self._send_loop())

    async def _init_irc(self):
        self.server       = self.config["irc"]["server"]
        self.nickname     = self.config["irc"]["nickname"]
        self.password     = self.config["irc"]["password"]
        self.main_channel = "#AzuraBot"

        self.irc_bot = botymcbotface.async_irc.IRCBot(self.nickname,
                                                      self.password,
                                                      debug_level=2)

        await self.irc_bot.connect(self.server, self.main_channel)
        
    async def _receive_loop(self):
        """This is the loop that receives messages for AzuraBot, that is,
        messages sent TO AzuraBot from the IRC server. It should NOT
        respond directly to messages it receives, instead it should
        forward them all to AzuraBot proper, to let it figure out what
        to do with them.

        """
        while True:
            msg = await self.irc_bot.get_msg(5)

            if not msg:
                continue

            if msg.msg_type == "PRIVMSG" and msg.channel == self.nickname:
                self.log(f"Private message: {msg.sender}->{msg.channel}: "
                         f"{msg.msg_text}")
                await self.irc_bot.privmsg(msg.sender, "Hello there.")

            if msg.msg_type == "PRIVMSG" and msg.channel != self.nickname:
                self.log(f"Channel message: {msg.sender} @ {msg.channel}: "
                         f"{msg.msg_text}")


    async def _send_loop(self):
        """This is the loop that sends messages from AzuraBot, that is,
        it gets messages from AzuraBot to send to the IRC server.
        """
        pass
