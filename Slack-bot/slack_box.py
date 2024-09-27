from cgi import test
import os
from typing import Optional
from pathlib import Path
import slack
from dotenv import load_dotenv
from data_box import Data_Box


class Slack_Box:
    def __init__(self) -> None:
        env_path = Path('..') / '.env'
        load_dotenv(dotenv_path=env_path)

        self.TUTOR_TOKEN: Optional[str] = os.getenv('TUTOR_SLACK_TOKEN')
        self.STUDENT_TOKEN: Optional[str] = os.getenv('STUDENT_SLACK_TOKEN')
        self.CHANNEL_ID: Optional[str] = os.getenv('PY_TUTOR_CHANNEL_ID')

        assert self.TUTOR_TOKEN is not None, "SLACK_TOKEN is not set in .env"
        assert self.CHANNEL_ID is not None, "PY_TUTOR_CHANNEL_ID is not set in .env"
        assert self.STUDENT_TOKEN is not None, "STUDENT_SLACK_TOKEN is not set in .env"

        self.tutor_client: slack.WebClient = slack.WebClient(
            token=self.TUTOR_TOKEN)

        self.student_client: slack.WebClient = slack.WebClient(
            token=self.STUDENT_TOKEN)

        self.data_box: Data_Box = Data_Box()

    def post_message(self, student_id: str, workspace_id: str, message: str, role: str = "Tutor") -> None:
        """
        Post a message to the Slack channel. If the student has a thread_ts, post the message in the thread.
        Otherwise create a new thread and post the message in the thread.

        Args:
            student_id (str): The student's ID.
            workspace_id (str): The workspace's ID.
            message (str): The message to post.
            role (str, optional): The role of the user posting the message. Defaults to "Tutor".

        Returns:
            None
        """

        thread_ts: Optional[str] = self.data_box.get_thread_ts(
            student_id=student_id, workspace_id=workspace_id)

        if role == "Tutor":
            client = self.tutor_client
        else:
            client = self.student_client

        if thread_ts is not None:
            response = client.chat_postMessage(
                channel=self.CHANNEL_ID, text=message, thread_ts=thread_ts)
        else:
            response = client.chat_postMessage(
                channel=self.CHANNEL_ID, text=message)
            thread_ts = response['ts']
            self.data_box.add_thread_ts_to_db(
                student_id=student_id, workspace_id=workspace_id, thread_ts=thread_ts)

        if not response['ok']:
            print(response['error'])
        else:
            print("Message sent successfully")
