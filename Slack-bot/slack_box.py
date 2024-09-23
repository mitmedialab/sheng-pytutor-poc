import os
from pathlib import Path
import slack
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

PY_TUTOR_CHANNEL_ID: str = "C07N96PA0F8"

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
post_message_data = client.chat_postMessage(
    channel=PY_TUTOR_CHANNEL_ID, text="I like apples.")
print(post_message_data)


def get_channel_history(channel_id: str) -> list:
    response = client.conversations_history(
        channel=channel_id, inclusive=True)
    messages = response['messages']
    return messages


# print(get_channel_history(PY_TUTOR_CHANNEL_ID))
