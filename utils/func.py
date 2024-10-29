from aiogram import types
from config import AUTH_SESSION, db
from keyboard.inline import kb_list_tasks


async def get_tasks_list(
    message: types.Message, title: str, status: int | None = None
) -> None:
    """Функция для вывода задач в виде инлайновых кнопок"""
    username = AUTH_SESSION.get(message.from_user.id)
    user_id = db.get_user(username)[0]
    tasks = (
        db.get_tasks(user_id, status)
        if status is not None
        else db.get_all_tasks(user_id)
    )
    title = title if tasks else "Задач нет"
    await message.answer(title, reply_markup=kb_list_tasks(tasks))
