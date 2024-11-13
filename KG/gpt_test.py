from data_box import Data_Box
from gpt_box import GPT_Box
import asyncio
import uuid
import json

data_box = Data_Box()

gpt_box = GPT_Box()


questions = [
    "How do I reverse a list?",
    """
    I am getting this piece of code wrong, what am I doing wrong here?
    ```py
    for i in range (10):
        print(list.get(i))
    ```
    """,
    """
    I think a list is mutable right? Because we can changes the values inside of the list somehow?
    """,
    """
    What is a dictionary and how do I access things inside of it?
    """,
    """
    I think I got the way of getting the value out from the dictionary.

    ```py
    test_dict = {
        'a': 4
    }

    print(test_dict['a'])
    ```
    """,
]


async def test_get_concept_from_student_question():
    """
    Tests questions and getting the concepts used for these questions
    """

    all_concepts = await data_box.get_all_concepts()

    for q in questions:
        changes = gpt_box.get_change_in_weight_for_question(q, all_concepts)
        print(q)
        print(changes)
        print()


async def test_get_tutor_response_from_student_weights(new_student_uuid: str):
    """
    Tests getting a tutor response from student weights
    """
    await data_box.add_new_student(new_student_uuid)

    for q in questions:
        changes = gpt_box.get_change_in_weight_for_question(q)
        change_dict = json.loads(changes)
        await data_box.change_student_weight(new_student_uuid, change_dict)
        student_weights = await data_box.get_student_weights(new_student_uuid)
        tutor_response = gpt_box.get_tutor_response_based_on_student_weight(
            q, student_weights
        )
        print(q)
        print(tutor_response)
        print()


if __name__ == "__main__":

    async def main():
        student = str(uuid.uuid4())
        # await test_get_concept_from_student_question()
        await data_box.connect_to_db()
        await test_get_tutor_response_from_student_weights(student)
        await data_box.close_connection()

    asyncio.run(main())
