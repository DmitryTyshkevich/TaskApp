from typing import List, Tuple
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


start_button = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Регистрация", callback_data="reg"),
            types.InlineKeyboardButton(text="Авторизация", callback_data="auth"),
        ],
    ]
)


def button_list_tasks(
    list_tasks: List[Tuple[int, int, str, str, int]]
) -> InlineKeyboardBuilder:
    """Создание динамических инлайновых кнопок для списка задач"""
    keyboard = InlineKeyboardBuilder()
    for task_id, _, title, _, status in list_tasks:
        text = f"{'✅' if status else '⏳'}{title}"
        keyboard.add(
            types.InlineKeyboardButton(text=text, callback_data=f"id_{task_id}")
        )
    return keyboard.adjust(3).as_markup()


def task_control(task_id: int, status: int) -> types.InlineKeyboardMarkup:
    """Создание кнопок управления задачей"""
    status_text = "Активировать" if status else "Завершить"
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Удалить", callback_data=f"del_{task_id}"
                ),
                types.InlineKeyboardButton(
                    text=status_text, callback_data=f"status_{status}_{task_id}"
                ),
            ],
        ]
    )
    return keyboard
