import os

import slack


def read_secret(section: str, file_name: str):
    with open(f"../secret/{section}/{file_name}") as f:
        return f.readline().strip()


slack_token = read_secret("slack", "oauth_access_token")

# rtmclient = slack.RTMClient(token=slack_token)
rtmclient = slack.RTMClient(token="foo")

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    print("input")
    data = payload['data']
    if 'Hello' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        webclient = payload['web_client']
        webclient.chat_postMessage(
            channel=channel_id,
            text="Hi <@{}>!".format(user),
            thread_ts=thread_ts
        )

rtmclient.start()
