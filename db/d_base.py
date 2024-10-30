import sqlite3
from typing import Optional, List, Tuple


class Database:
    """Класс для управления взаимодействием с базой данных SQLite, содержащей
    таблицы для хранения информации о пользователях и их задачах."""

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
                username TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status INTEGER DEFAULT 0,
                FOREIGN KEY (username) REFERENCES users(username)
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

    def add_task(self, username: str, title: str, description: str) -> None:
        """Добавить новую задачу для пользователя."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (username, title, description) VALUES (?, ?, ?)",
                (username, title, description),
            )

    def get_all_tasks(self, username: str) -> List[Tuple[int, str, str, str, int]]:
        """Получить все задачи пользователя."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE username = ?", (username,))
            tasks = cursor.fetchall()
        return tasks

    def get_tasks(
        self, username: str, status: int
    ) -> List[Tuple[int, str, str, str, int]]:
        """Получить активные или завершенные задачи пользователя."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tasks WHERE username = ? AND status = ?",
                (username, status),
            )
            tasks = cursor.fetchall()
        return tasks

    def get_task(self, task_id: int) -> Optional[Tuple[int, str, str, str, int]]:
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
