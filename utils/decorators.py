from functools import wraps
from typing import Callable, Union
from aiogram import types
from aiogram.fsm.context import FSMContext
from config import AUTH_SESSION
from fsm.FSM import AuthUser


def authorized_only(func: Callable) -> Callable:
    """Декоратор для проверки авторизации"""

    @wraps(func)
    async def wrapper(
        update: Union[types.Message, types.CallbackQuery],
        state: FSMContext,
        *args,
        **kwargs
    ) -> None:

        user_id = (
            update.from_user.id
            if isinstance(update, types.Message)
            else update.message.chat.id
        )

        if AUTH_SESSION.get(user_id) is not None:
            return await func(update, state, *args, **kwargs)

        text = "Вы не авторизованы. Пожалуйста, введите логин:"

        if isinstance(update, types.Message):
            await update.answer(text)
            await state.set_state(AuthUser.username)
        elif isinstance(update, types.CallbackQuery):
            await update.message.answer(text)
            await state.set_state(AuthUser.username)

    return wrapper
