from aiogram.fsm.state import StatesGroup, State


class AddUser(StatesGroup):
    """Состояния для добавления нового пользователя."""

    name = State()
    username = State()


class AythUser(StatesGroup):
    """Состояния для авторизации пользователя"""

    username = State()


class AddTask(StatesGroup):
    """Состояния для добавления новой задачи"""

    title = State()
    description = State()
