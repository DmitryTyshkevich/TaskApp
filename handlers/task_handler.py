from aiogram import F, types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from fsm.FSM import AddTask
from config import db, AUTH_SESSION
from utils.decorators import authorized_only


task_router = Router()


@task_router.message(StateFilter(None), F.text == "Создать задачу")
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
