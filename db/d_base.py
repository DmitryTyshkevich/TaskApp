import sqlite3
from typing import Optional, List, Tuple


class Database:
    def __init__(self, db_path: str) -> None:
        """Инициализация соединения с базой данных."""
        self.db_path = db_path
        self.create_tables()

    def create_tables(self) -> None:
        """Создание таблиц для пользователей и задач."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL
            )
            """
            )
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """
            )

    def add_user(self, username: str, name: str) -> None:
        """Добавить нового пользователя в базу данных."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, name) VALUES (?, ?)",
                (username, name),
            )

    def get_user(self, username: str) -> Optional[Tuple[int, str, str]]:
        """Получить пользователя по его логину."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
        return user

    def add_task(self, user_id: int, title: str, description: str) -> None:
        """Добавить новую задачу для пользователя."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
                (user_id, title, description),
            )

    def get_all_tasks(self, user_id: int) -> List[Tuple[int, int, str, str, int]]:
        """Получить все задачи пользователя."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
            tasks = cursor.fetchall()
        return tasks

    def get_tasks(
        self, user_id: int, status: int
    ) -> List[Tuple[int, int, str, str, int]]:
        """Получить активные или завершенные задачи пользователя."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tasks WHERE user_id = ? AND status = ?",
                (user_id, status),
            )
            tasks = cursor.fetchall()
        return tasks

    def get_task(self, task_id: int) -> Optional[Tuple[int, int, str, str, int]]:
        """Получить конкретную задачу"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            task = cursor.fetchone()
        return task

    def update_task_status(self, task_id: int, status: int) -> None:
        """Обновить статуса задачи."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET status = ? WHERE id = ?", (status, task_id)
            )

    def delete_task(self, task_id: int) -> None:
        """Удаление задачи по её идентификатору."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
