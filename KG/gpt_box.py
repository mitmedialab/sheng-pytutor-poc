import os
from typing import Union
from pathlib import Path
from dotenv import load_dotenv
import requests

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)


class GPT_Box:
    def __init__(self) -> None:
        self.gpt_token = os.environ['GPT_TOKEN']
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.upload_file_url = "https://api.openai.com/v1/uploads"

    def send_message(self, message: str) -> Union[dict, str]:
        """
        Send a message to the GPT-4o model and get a response.
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.gpt_token}'
        }
        data = {
            'model': 'gpt-4o',

            'messages': [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    'role': 'user',
                    'content': message
                }
            ]
        }

        response = requests.post(
            self.api_url,
            json=data,
            headers=headers,
            timeout=10
        )

        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else response.text
