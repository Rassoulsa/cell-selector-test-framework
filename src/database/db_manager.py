import sqlite3
from pathlib import Path

from database.schema import SCHEMA_SQL


class DatabaseManager:
    def __init__(self, db_path: str = "test_results.db"):
        self.db_path = db_path
        self._ensure_database()

    def _ensure_database(self) -> None:
        db_file = Path(self.db_path)

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.executescript(SCHEMA_SQL)
            conn.commit()

    def insert_test_run(
        self,
        run_date: str,
        total: int,
        passed: int,
        failed: int,
        errors: int,
    ) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO test_runs (run_date, total, passed, failed, errors)
                VALUES (?, ?, ?, ?, ?)
                """,
                (run_date, total, passed, failed, errors),
            )
            conn.commit()
            return cursor.lastrowid

    def insert_test_result(
        self,
        run_id: int,
        test_name: str,
        status: str,
        duration: float,
        message: str = "",
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO test_results (run_id, test_name, status, duration, message)
                VALUES (?, ?, ?, ?, ?)
                """,
                (run_id, test_name, status, duration, message),
            )
            conn.commit()

    def get_all_test_runs(self) -> list[tuple]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, run_date, total, passed, failed, errors
                FROM test_runs
                ORDER BY id DESC
                """
            )
            return cursor.fetchall()

    def get_results_for_run(self, run_id: int) -> list[tuple]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT test_name, status, duration, message
                FROM test_results
                WHERE run_id = ?
                ORDER BY id ASC
                """,
                (run_id,),
            )
            return cursor.fetchall()