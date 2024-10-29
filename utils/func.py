from aiogram import types
from config import AUTH_SESSION, db
from keyboard.inline import button_list_tasks


async def get_tasks_list(
    message: types.Message, title: str, status: int | None = None
) -> None:
    """Функция для вывода задач в виде инлайновых кнопок"""
    username = AUTH_SESSION.get(message.from_user.id)
    tasks = (
        db.get_tasks(username, status)
        if status is not None
        else db.get_all_tasks(username)
    )
    title = title if tasks else "Задач нет"
    await message.answer(title, reply_markup=button_list_tasks(tasks))
