import os
from typing import Union
from pathlib import Path
from dotenv import load_dotenv
import requests

env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)


class GPT_Box:
    def __init__(self) -> None:
        self.gpt_token = os.environ["GPT_TOKEN"]
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.upload_file_url = "https://api.openai.com/v1/uploads"

    def send_message(
        self, message: str, LLM_personality="You are a helpful assistant"
    ) -> Union[dict, str]:
        """
        Send a message to the GPT-4o model and get a response.
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.gpt_token}",
        }
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": LLM_personality},
                {"role": "user", "content": message},
            ],
        }

        response = requests.post(self.api_url, json=data, headers=headers, timeout=10)

        return (
            response.json()["choices"][0]["message"]["content"]
            if response.status_code == 200
            else response.text
        )

    def get_change_in_weight_for_question(
        self, student_question: str, concepts_list=list[str]
    ) -> list[int]:
        LLM_Prompt_part_one = """
        You are a very specific and strict grader of questions.

        You will be given a question or a thought that a student has had and your responsibility is to return back to me a list of concepts that the question / thought that the student has used in this question along with a score from -3 to +3. You would give a very high score if you think the student understands the problem very much and you would give a very low score if you think the student does not understand the concept at all based solely on their question / thought.

        As an example a student might ask you: "what is a list and how do I loop through it?" You would return me back a json that may looks something like this:

            {
                "list indexing": -2,
                "list creation": -1,
                .... (some more concepts)
            }

        However, one important part is for you to only pick out concepts from these available concepts to return back to me. You can pick out a max of 5 most relevant concepts. Do not include irrelevant concepts. These are the available concepts to choose from:
        """

        available_concepts = str(concepts_list)

        LLM_Prompt_part_two = "ONLY RETURN THE JSON STRING WITH NO JSON QUOTES AROUND THEM. DO NOT RETURN ME ANYTHING ELSE."

        combined_prompt = LLM_Prompt_part_one + available_concepts + LLM_Prompt_part_two

        return self.send_message(student_question, combined_prompt)

    def get_tutor_response_based_on_student_weight(
        self, student_question: str, student_weights: str
    ) -> str:
        LLM_PROMPT_PART_ONE = """
        You are a tutor who is trying to help a student understand a concept better. You have been given a set of weights for a student and you are to return back to me a response that will help the student understand the concept better. You can use the weights to determine what the student does not understand and what the student understands well. The weights are in a json string format with key: value pair representing the concepts and the weights. The higher the weight, the better the student understands that concept. Here is an example of what the weights might look like:
                
            {
                "list indexing": 2,
                "list creation": -3,
                .... (some more concepts)
            }

        And here is an example of a student question that you might be given:

            "What is a list and how do I loop through it?"

        And you might return back to me a response that looks something like this:
            
                "I see that you had some trouble with list creations. Do you want me to explain that to you?"

        These are the actual data. You can use this to help you generate a response to the student. You can use the weights to determine what the student understands and what the student does not understand. Also, do not let the students know that you are basing your response on the weights that they have given you.

        A good way to guide students is by not giving away answers but ask them lots of questions. 
        """

        LLM_PROMPT_PART_TWO = f"Question: {
            student_question}\nWeights: {student_weights}"

        total_prompt = LLM_PROMPT_PART_ONE + LLM_PROMPT_PART_TWO

        return self.send_message(student_question, total_prompt)
