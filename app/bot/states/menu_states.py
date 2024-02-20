from aiogram.fsm.state import StatesGroup, State


class MenuStates(StatesGroup):
    choosing_option = State()
    choosing_category = State()
    choosing_difficulty = State()
