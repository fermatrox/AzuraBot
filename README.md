# AzuraBot overview

AzuraBot is an plugin-based Open Source chatbot framework, written in
Python using the `asyncio` package. It can be used in two different ways:
- As a backend and middleware
- As a backend only

# Installation

AzuraBot has only been tested on Linux. It requires Python 3.7 or
newer, and uses
[BotyMcBotface](https://github.com/Enfors/BotyMcBotface) for its IRC
interface. Install it with `pip` (I recommend using a virtual
environment):

    $ pip install BotyMcBotface

Then, you need to register its IRC nickname (read: your bot's IRC
username). I recommend using the Freenode IRC network, and there's a
guide on how to register a nickname on Freenode
[here](http://www.wikihow.com/Register-a-Nickname-on-Freenode). It
doesn't matter what nickname you decide to use, but remember that it
is this name that your instance of AzuraBot will have on IRC.

# Configuration

In AzuraBot's `etc` directory, there's an example configuration file
called `example-azurabot.conf`. Copy it to `azurabot.conf`:

    $ cd etc
    $ cp example-azurabot.conf azurabot.conf
    
Then, you have to edit `azurabot.conf` and insert your bot's nickname
and password, which you presumably registered using the guide above,
under the `[irc]` heading.

# Starting the bot

Then, you should be able to start it with the start script:

    $ cd ..
    $ ./start.sh

Press `Ctrl-c` to stop it.

To test if it works, fire up your favorite IRC client and send a
message to the bot:

    /msg (Your bot's nickname here) Status

# Architecture

AzuraBot supports different types of plugins, which must also be
written in Python. 

## Interface plugins

Interface plugins are what gives AzuraBot the ability to communicate
with user. Each such plugin makes it possible for users to communicate
with AzuraBot using a specific protocol or service, for example IRC,
Slack, or Twitter.

## Intent selector plugins

Intent selector plugins have the role of selecting an intent for input
sent to AzuraBot by a user. That is, what is the "intent" of the
user - what do they want? Is their intent to get a weather report, or
to create a reminder?

## Intent plugins

Intent plugins provide the intents, or actions if you will, that the
user can request to have performed.

## Filter plugins

