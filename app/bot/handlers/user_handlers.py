from aiogram import Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.bot.keyboards import KeyboardManager
from app.bot.states.menu_states import MenuStates
from app.logs import logger


class UserHandler:
    __slots__ = "dp", "router"

    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.router = Router()
        self.dp.include_router(self.router)

    def register_handlers(self):
        logger.info("Register user handlers")

        # Логика проверки почты в таблице
        self.router.message.register(self.start, Command('start'))  # регистрация хэндлера для команды старт

        self.router.callback_query.register(self.back_to_main_menu, F.data == 'back-to-main-menu')

    async def start(self, message: Message, state: FSMContext):
        """ Хэндлер для команды старт """
        logger.info(
            f"START Handler {message.chat.id}  {message.from_user.username} {message.text}")

        text = "Главное меню"
        await message.answer(text=text, reply_markup=KeyboardManager.main_menu())
        await state.set_state(MenuStates.choosing_option)


    async def back_to_main_menu(self, callback: CallbackQuery, state: FSMContext):
        logger.info(f'user {callback.from_user.full_name} with id {callback.from_user.id} back to main menu')

        await callback.message.edit_text('Главное меню')
        await callback.message.edit_reply_markup(reply_markup=KeyboardManager.main_menu())
        await state.set_state(MenuStates.choosing_option)
