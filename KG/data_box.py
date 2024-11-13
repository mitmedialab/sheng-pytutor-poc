from pathlib import Path
import os
import asyncpg
import asyncio
import uuid
import json

from dotenv import load_dotenv

env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)


class Data_Box:
    def __init__(self):
        self.dbname: str = os.getenv("DB_NAME")
        self.user: str = os.getenv("DB_USER")
        self.password: str = os.getenv("DB_PASSWORD")
        self.host: str = os.getenv("DB_HOST")
        self.port: str = os.getenv("DB_PORT")
        self.table_name: str = os.getenv("DB_TABLE_NAME")
        self.connection = None
        self.all_concept_names = None

    async def connect_to_db(self) -> None:
        """
        Connect to the database.
        """
        if self.connection is None:
            self.connection = await asyncpg.connect(
                user=self.user,
                password=self.password,
                database=self.dbname,
                host=self.host,
                port=self.port,
            )
            print("Connected to the database.")

    async def close_connection(self) -> None:
        """
        Close the connection to the database.
        """
        if self.connection is not None:
            await self.connection.close()
            self.connection = None
            print("Connection to the database closed.")
        else:
            print("No connection to close.")

    async def get_student_weights(self, uuid) -> str:
        """
        Get the weights of a student.

        Returns a JSON string of the weights.
        """

        query = f"SELECT * FROM {self.table_name} WHERE id = '{uuid}';"
        res = await self.connection.fetch(query)

        res_dict = [dict(record) for record in res]
        for record in res_dict:
            del record["id"]
        res_json = json.dumps(res_dict[0])
        return res_json

    async def add_new_student(self, uuid):
        """
        Add a new student to the database.
        """

        query = f"INSERT INTO {self.table_name} (id) VALUES ('{uuid}')"
        await self.connection.execute(query)
        print(f"Student {uuid} added.")

    async def get_all_concepts(self):
        query = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{self.table_name}';
        """
        res = await self.connection.fetch(query)
        all_concept_names = {record['column_name'] for record in res} - {"id"}
        return all_concept_names

    async def change_student_weight(self, uuid, concept_names: dict):
        """
        Change the weight of a concept for a student.
        """

        if self.all_concept_names is None:
            self.all_concept_names = await self.get_all_concepts()

        # get a set of all the headers in the table

        if len(concept_names) == 0:
            return

        # update the weight of the concept
        query = f"UPDATE {self.table_name} SET "
        for concept_name, value in concept_names.items():
            if concept_name not in self.all_concept_names:
                continue
            query += f"{concept_name} = {value}, "
        query = query[:-2] + f" WHERE id = '{uuid}';"

        print(f"Student {uuid} weights updated.")


if __name__ == "__main__":

    async def main():
        box = Data_Box()
        fake_uuid = str(uuid.uuid4())
        # await box.add_new_student(fake_uuid)
        # print(await box.get_student_weights(fake_uuid))

    asyncio.run(main())
