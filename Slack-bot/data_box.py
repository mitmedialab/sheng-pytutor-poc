
from typing import Optional


class Data_Box:
    def __init__(self) -> None:
        pass

    def get_thread_ts(self, student_id: str, workspace_id: str) -> Optional[str]:
        pass

    def add_thread_ts_to_db(self, student_id: str, workspace_id: str, thread_ts: str) -> None:
        pass
