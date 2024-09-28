import asyncpg
from typing import Optional


class Data_Box:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    async def connect(self) -> None:
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

    async def get_thread_ts(self, student_id: str, workspace_id: str) -> Optional[str]:
        """
        Get the thread_ts from the database using {student_id}_{workspace_id} as the key.

        Args:
            student_id (str): The student's ID.
            workspace_id (str): The workspace's ID.

        Returns:
            Optional[str]: The thread_ts if it exists, otherwise None.

        """
        db_key: str = f"{student_id}_{workspace_id}"
        query: str = "SELECT thread_ts FROM students WHERE student_id = $1;"
        thread_ts = await self.connection.fetchval(query, db_key)
        return thread_ts

    async def add_thread_ts_to_db(self, student_id: str, workspace_id: str, thread_ts: str) -> None:
        """
        Add a thread_ts to the database using {student_id}_{workspace_id} as the key.

        Args:
            student_id (str): The student's ID.
            workspace_id (str): The workspace's ID.
            thread_ts (str): The thread_ts to add to the database.

        Returns:
            None

        """
        db_key: str = f"{student_id}_{workspace_id}"
        query: str = "INSERT INTO students (student_id, thread_ts) VALUES ($1, $2) ON CONFLICT (student_id) DO UPDATE SET thread_ts = EXCLUDED.thread_ts;"
        await self.connection.execute(query, db_key, thread_ts)

    async def close(self) -> None:
        """
        Close the connection to the database.
        Should be called when the program is done using the database.
        """
        if self.connection:
            await self.connection.close()
            print("Connection to the database closed.")
        else:
            print("No connection to close.")
