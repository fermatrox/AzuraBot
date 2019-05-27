#!/usr/bin/env python

"""
Based on https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
and also https://github.com/slackapi/python-slackclient/wiki/Migrating-to-2.x.

At the moment, this doesn't work. See slack_test2 instead.
"""

import os
import time
import re

from slack import WebClient

# Instantiate Slack client

def read_secret(section: str, file_name: str):
    with open(f"../secrets/{section}/{filename}") as f:
        return f.readline().strip()


token = read_secret("slack", "oauth_access_token")

slack_client = SlackClient(token)

# AzuraBot's user ID in Slack; value is assigned after the bot starts up.
azurabot_id = None

# Constants
RTM_READ_DELAY = 1
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == azurabot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # first group: username, second group: remaining message
    return (matches.group(1), matches.group(2).strip) if \
        matches else (None, None)


def handle_command(command, channel):
    default_response = f"Not sure what you mean. Try *{EXAMPLE_COMMAND}*."

    response = None
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure, just add the code for it first."

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("AzuraBot connected and running.")
        # Read bot's user ID by calling Web API method 'auth.test'
        azurabot_id = slack_client.api_call("auth.text")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
