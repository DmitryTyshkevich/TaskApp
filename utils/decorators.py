from functools import wraps
from typing import Callable
from aiogram import types
from config import AUTH_SESSION
from keyboard.inline import start_button


def authorized_only(func: Callable) -> Callable:
    """Декоратор для проверки авторизации"""

    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs) -> None:
        user_id = message.from_user.id
        if AUTH_SESSION.get(user_id) is not None:
            return await func(message, *args, **kwargs)
        await message.answer(
            "Вы не авторизованы. Пожалуйста, пройдите авторизацию.",
            reply_markup=start_button,
        )

    return wrapper
