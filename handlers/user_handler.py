from aiogram import F, types, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from fsm.FSM import AddUser, AythUser
from keyboard.inline import start_button
from keyboard.reply import reply_keyboard
from config import AUTH_SESSION, db


user_router = Router()


@user_router.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    """Обработчик команды /start"""
    await message.answer(
        "👋 Здравствуйте! Пройдите регистрацию или авторизуйтесь:",
        reply_markup=start_button,
    )


@user_router.callback_query(StateFilter(None), F.data == "reg")
async def enter_name(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Обработчик инлайновой кнопки для регистрации"""
    await callback.answer()
    await callback.message.answer("Введите имя:")
    await state.set_state(AddUser.name)


@user_router.message(AddUser.name, F.text)
async def get_name(message: types.Message, state: FSMContext) -> None:
    """Функция для обработки имени при регистрации"""
    if message.text.isalpha() and 2 <= len(message.text) <= 30:
        name = message.text.title()
        await state.update_data(name=name)
        await message.answer("Теперь введите логин:")
        await state.set_state(AddUser.username)
    else:
        await message.answer("Введите корректное имя:")


@user_router.message(AddUser.name)
async def rename(message: types.Message, state: FSMContext) -> None:
    """Обработчик некорректного ввода имени при регистрации"""
    await message.answer("Введите имя:")


@user_router.message(AddUser.username, F.text)
async def get_username(message: types.Message, state: FSMContext) -> None:
    """Функция для обработки логина при регистрации"""
    user_id = message.from_user.id
    username = message.text
    if db.get_user(username):
        await message.answer("Этот логин уже занят. Пожалуйста, выбери другой.")
    else:
        data = await state.get_data()
        name = data.get("name")
        db.add_user(username, name)
        AUTH_SESSION[user_id] = username

        await message.answer(
            f"{name}, регистрация прошла успешно!", reply_markup=reply_keyboard
        )
        await state.clear()


@user_router.message(AddUser.username)
async def reusername(message: types.Message, state: FSMContext) -> None:
    """Обработчик некорректного ввода логина при регистрации"""
    await message.answer("Введите логин:")


@user_router.callback_query(StateFilter(None), F.data == "auth")
async def aythentication(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Обработчик инлайновой кнопки для авторизации"""
    await callback.answer()
    await callback.message.answer("Введите логин:")
    await state.set_state(AythUser.username)


@user_router.message(AythUser.username, F.text)
async def enter_username_for_auth(message: types.Message, state: FSMContext) -> None:
    """Функция для обработки логина при авторизации"""
    user_id = message.from_user.id
    username = message.text
    if db.get_user(username):
        AUTH_SESSION[user_id] = username
        await message.answer("Вы успешно авторизовались", reply_markup=reply_keyboard)
        await state.clear()
    else:
        await message.answer(
            "Совпадений не найдено, пройдите регистрацию либо повторите попытку:",
            reply_markup=start_button,
        )
        await state.clear()


@user_router.message(AythUser.username)
async def enter_username(message: types.Message, state: FSMContext) -> None:
    """Обработчик некорректного ввода логина при авторизации"""
    await message.answer("Введите логин:")


@user_router.message()
async def other(message: types.Message) -> None:
    """Обработчик неосмысленного ввода пользователем"""
    await message.answer("Выберите действие или введите команду /start")
