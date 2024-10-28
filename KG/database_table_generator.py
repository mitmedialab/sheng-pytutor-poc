from pathlib import Path
import os
import asyncpg
import yaml
import asyncio

from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)


class Database_Table_Generator:
    def __init__(self):
        self.all_concepts_path: str = Path("all_concepts.yml")
        self.dbname: str = os.getenv("DB_NAME")
        self.user: str = os.getenv("DB_USER")
        self.password: str = os.getenv("DB_PASSWORD")
        self.host: str = os.getenv("DB_HOST")
        self.port: str = os.getenv("DB_PORT")
        self.connection = None

    async def connect_to_db(self) -> None:
        """
        Connect to the database.
        """
        self.connection = await asyncpg.connect(
            user=self.user,
            password=self.password,
            database=self.dbname,
            host=self.host,
            port=self.port
        )

        if self.connection is not None:
            print("Connected to the database.")
        else:
            print("Failed to connect to the database.")

    async def close_connection(self) -> None:
        """
        Close the connection to the database.
        """
        if self.connection:
            await self.connection.close()
            print("Connection to the database closed.")
        else:
            print("No connection to close.")

    async def create_table(self) -> None:
        """
        Create a table in the database.
        """

        if self.connection is None:
            await self.connect_to_db()

        with open(self.all_concepts_path, "r") as file:
            all_concepts = yaml.safe_load(file)
            table_name = "Concepts"
            query = f"CREATE TABLE IF NOT EXISTS {
                table_name} (kerb VARCHAR(255) PRIMARY KEY,"

            for concept in all_concepts:
                query += f"{concept} int,"
            query = query[:-1] + ");"
            await self.connection.execute(query)
            print(f"Table {table_name} created.")

        await self.close_connection()


if __name__ == "__main__":
    async def main():
        db_table_generator = Database_Table_Generator()
        await db_table_generator.create_table()

    asyncio.run(main())
