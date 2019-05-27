import os

import slack


def read_secret(section: str, file_name: str):
    with open(f"../secret/{section}/{file_name}") as f:
        return f.readline().strip()


slack_token = read_secret("slack", "bot_user_oauth_access_token")

# rtmclient = slack.RTMClient(token=slack_token)
rtmclient = slack.RTMClient(token=slack_token)

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    print("input")
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'Hello' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        webclient.chat_postMessage(
            channel=channel_id,
            text="Hi <@{}>!".format(user),
            thread_ts=thread_ts
        )

print("Running.")
rtmclient.start()
