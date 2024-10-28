from aiogram import types


reply_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Создать задачу"),
            types.KeyboardButton(text="Все задачи"),
        ],
        [
            types.KeyboardButton(text="Активные"),
            types.KeyboardButton(text="Завершенные"),
        ],
    ],
    resize_keyboard=True,
)
