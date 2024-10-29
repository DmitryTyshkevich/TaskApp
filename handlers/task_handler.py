from aiogram import F, types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from fsm.FSM import AddTask
from config import db, AUTH_SESSION
from keyboard.inline import task_control
from utils.decorators import authorized_only
from utils.func import get_tasks_list


task_router = Router()


@task_router.message(StateFilter(None), F.text.lower() == "создать задачу")
@authorized_only
async def enter_title(message: types.Message, state: FSMContext) -> None:
    """Функция для ввода названия задачи"""
    await message.answer("Введите название задачи")
    await state.set_state(AddTask.title)


@task_router.message(AddTask.title, F.text)
async def get_title(message: types.Message, state: FSMContext) -> None:
    """Функция для получения названия задачи"""
    title = message.text
    await state.update_data(title=title)
    await message.answer("Теперь введите описание задачи")
    await state.set_state(AddTask.description)


@task_router.message(AddTask.title)
async def retitle(message: types.Message, state: FSMContext) -> None:
    """Обработка некорректного ввода названия задачи"""
    await message.answer("Введите корректное название задачи")


@task_router.message(AddTask.description, F.text)
async def get_description(message: types.Message, state: FSMContext):
    if not len(message.text) <= 5:
        description = message.text
        username = AUTH_SESSION.get(message.from_user.id)
        user_id = db.get_user(username)[0]
        data = await state.get_data()
        title = data.get("title")
        db.add_task(user_id, title, description)
        await message.answer("Задача добавлена!")
        await state.clear()
    else:
        await message.answer("Введите более содержательное описание")


@task_router.message(AddTask.description)
async def redescription(message: types.Message, state: FSMContext) -> None:
    """Обработка некорректного ввода описания задачи"""
    await message.answer("Введите корректное описание задачи")


@task_router.message(StateFilter(None), F.text.lower() == "все задачи")
@authorized_only
async def get_all_tasks(message: types.Message, state: FSMContext) -> None:
    """Выводит список всех задач в виде инлайновых кнопок"""
    title = "Список всех задач:"
    await get_tasks_list(message, title)


@task_router.message(StateFilter(None), F.text.lower() == "активные")
@authorized_only
async def get_tasks_active(message: types.Message, state: FSMContext) -> None:
    """Выводит список активных задач в виде инлайновых кнопок"""
    title = "Список активных задач:"
    await get_tasks_list(message, title, 0)


@task_router.message(StateFilter(None), F.text.lower() == "завершенные")
@authorized_only
async def get_tasks_completed(message: types.Message, state: FSMContext) -> None:
    """Выводит список завершенных задач в виде инлайновых кнопок"""
    title = "Список завершенных задач:"
    await get_tasks_list(message, title, 1)


@task_router.callback_query(StateFilter(None), F.data.startswith("id_"))
@authorized_only
async def get_task(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Вывод конкретной задачи"""
    await callback.answer()
    task_id = int(callback.data.split("_")[-1])
    task = db.get_task(task_id)
    if task is None:
        await callback.message.answer("Задача не найдена.")
        return
    title = task[2]
    description = task[3]
    status = task[-1]
    status_text = "✅ Завершенная" if status else "⏳ Активная"
    await callback.message.answer(
        f"<strong>Название задачи:</strong> {title}\n<strong>Статус:</strong> {status_text}\n\n<strong>Описание задачи:</strong>\n{description}",
        reply_markup=task_control(task_id, status),
    )


@task_router.callback_query(StateFilter(None), F.data.startswith("del_"))
@authorized_only
async def del_task(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Удалить задачу"""
    task_id = int(callback.data.split("_")[-1])
    db.delete_task(task_id)
    await callback.message.delete()
    await callback.message.answer("Задача удалена")


@task_router.callback_query(StateFilter(None), F.data.startswith("status_"))
@authorized_only
async def change_status(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Изменить статус"""
    _, current_status, task_id = callback.data.split("_")
    status = 1 if not int(current_status) else 0
    db.update_task_status(int(task_id), int(status))
    await callback.message.delete()
    await callback.message.answer("Статус изменен")
