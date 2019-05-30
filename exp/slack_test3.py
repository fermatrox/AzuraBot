import os
import pprint

import slack


def read_secret(section: str, file_name: str):
    with open(f"../secret/{section}/{file_name}") as f:
        return f.readline().strip()

pp = pprint.PrettyPrinter(indent=4)


@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    print("input")
    data = payload['data']
    pp.pprint(data)
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if "text" in data and "Hello" in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text="Hi <@{}>!".format(user),
            thread_ts=thread_ts
        )

slack_token = read_secret("slack", "bot_user_oauth_access_token")

# rtmclient = slack.RTMClient(token=slack_token)
rtmclient = slack.RTMClient(token=slack_token)
print("Token:", slack_token)

print("Starting.")
rtmclient.start()
print("Exiting.")
