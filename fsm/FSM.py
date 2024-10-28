from aiogram.fsm.state import StatesGroup, State


class AddUser(StatesGroup):
    name = State()
    username = State()


class AythUser(StatesGroup):
    username = State()


class AddTask(StatesGroup):
    title = State()
    description = State()