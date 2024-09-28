import os
import asyncio
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

        self.DB_Name: Optional[str] = os.getenv('DB_NAME')
        self.DB_User: Optional[str] = os.getenv('DB_USER')
        self.DB_Password: Optional[str] = os.getenv('DB_PASSWORD')
        self.DB_Host: Optional[str] = os.getenv('DB_HOST')
        self.DB_Port: Optional[str] = os.getenv('DB_PORT')

        self.check_init()

        self.tutor_client: slack.WebClient = slack.WebClient(
            token=self.TUTOR_TOKEN)

        self.student_client: slack.WebClient = slack.WebClient(
            token=self.STUDENT_TOKEN)

        self.data_box: Data_Box = Data_Box(
            dbname=self.DB_Name,
            user=self.DB_User,
            password=self.DB_Password,
            host=self.DB_Host,
            port=self.DB_Port
        )

    def check_init(self) -> None:
        """
        Check if the Slack_Box was initialized correctly.

        Returns:
            None
        """
        assert self.TUTOR_TOKEN is not None, "SLACK_TOKEN is not set in .env"
        assert self.CHANNEL_ID is not None, "PY_TUTOR_CHANNEL_ID is not set in .env"
        assert self.STUDENT_TOKEN is not None, "STUDENT_SLACK_TOKEN is not set in .env"
        assert self.DB_Name is not None, "DB_NAME is not set in .env"
        assert self.DB_User is not None, "DB_USER is not set in .env"
        assert self.DB_Password is not None, "DB_PASSWORD is not set in .env"
        assert self.DB_Host is not None, "DB_HOST is not set in .env"
        assert self.DB_Port is not None, "DB_PORT is not set in .env"

    async def post_message(self, student_id: str, workspace_id: str, message: str, role: str = "Tutor") -> None:
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

        thread_ts: Optional[str] = await self.data_box.get_thread_ts(
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
            await self.data_box.add_thread_ts_to_db(
                student_id=student_id, workspace_id=workspace_id, thread_ts=thread_ts)

        if not response['ok']:
            print(response['error'])
        else:
            print("Message sent successfully")


if __name__ == "__main__":
    async def main():
        """
        Test the Slack_Box class.
        """
        test_box = Slack_Box()
        await test_box.data_box.connect()
        await test_box.post_message("123", "456", "DB Test")
        await test_box.data_box.close()

    asyncio.run(main())
