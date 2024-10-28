from aiogram import types


start_button = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Регистрация", callback_data="reg"),
            types.InlineKeyboardButton(text="Авторизация", callback_data="auth"),
        ],
    ]
)
