from aiogram import Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatJoinRequest

from app.bot.keyboards import KeyboardManager
from app.bot.states.menu_states import MenuStates
from app.db.session import LocalSession
from app.logs import bot_log


class UserHandler:
    __slots__ = "dp", "router"
    current_user_request = {}

    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.router = Router()
        self.dp.include_router(self.router)

    def register_handlers(self):
        bot_log.info("Register user handlers")

        # Логика проверки почты в таблице
        self.router.message.register(self.start, Command('start'))  # регистрация хэндлера для команды старт

        self.router.message.register(self.help, Command('help'))  # регистрация хэндлера для команды хэлп

        self.router.channel_post.register(self.test_inline_in_channel, Command('post'),
                                          # регистрация хэндлера для команды пост
                                          F.chat.type == 'channel')  # с фильтром только для каналов

        self.router.callback_query.register(self.message_actions_change_content_on_count,
                                            # регистрация хэндлера для команды
                                            F.data == 'change-content-on-count')  # с фильтром на значение колбэк дата

        self.router.chat_join_request.register(self.auto_approve_handler,
                                               F.chat.type == 'channel')  # регистрация хэндлера для отправки приветственного сообщению пользователю при заявке в закрытый канал

        self.router.callback_query.register(self.back_to_main_menu, F.data == 'back-to-main-menu')

    async def start(self, message: Message, state: FSMContext):
        """ Хэндлер для команды старт """
        bot_log.info(
            f"START Handler {message.chat.id}  {message.from_user.username} {message.text}")
        current_join_request = self.current_user_request.get(message.from_user.id)
        async with LocalSession() as db:
            if current_join_request:
                await current_join_request.approve()
                await add_user_in_db_by_join_request(db, current_join_request, message)
                self.current_user_request.pop(message.from_user.id)
            else:
                await add_user_in_db_by_ref_link(db, message)

        text = "Главное меню"
        await message.answer(text=text, reply_markup=KeyboardManager.main_menu())
        await state.set_state(MenuStates.choosing_option)

    async def help(self, message: Message):
        """ Хэндлер для команды хэлп """
        bot_log.info(
            f'HELP Handler {message.chat.id} {message.from_user.username} {message.text}'
        )

        await message.answer(text='Нажмите, чтобы получить информацию', reply_markup=KeyboardManager.help_keyboard())

    async def test_inline_in_channel(self, channel_post: Message):
        """ Хэндлер для отправки тестового сообщения с инлайн кнопками """
        bot_log.info(
            f'TEST_INLINE_IN_CHANNEL {channel_post.chat.id} {channel_post.text}')
        bot_log.info(
            f'{channel_post.chat.model_dump()}'
        )
        await channel_post.answer(text='Выберете кнопку', reply_markup=KeyboardManager.post_keyboard())

    async def message_actions_change_content_on_count(self, callback: CallbackQuery):
        """ Хэндлер для обработки колбэков с датой change-content-on-count """
        bot_log.info(
            f'MESSAGE_ACTIONS_CHANGE_CONTENT_ON_COUNT callback_data - {callback.data}; callback_id - {callback.id}')
        await callback.answer("Вы нажали на кнопку... ")

    async def auto_approve_handler(self, update: ChatJoinRequest):
        bot_log.info(f'AUTO_APPROVE_HANDLER update from user - {update.from_user.username} ({update.from_user.id})')

        user_id = update.from_user.id

        self.current_user_request[update.from_user.id] = update
        await update.bot.send_message(user_id, text='Для завершения регистрации нажмите кнопку /start',
                                      reply_markup=KeyboardManager.register_keyboard())

    async def back_to_main_menu(self, callback: CallbackQuery, state: FSMContext):
        bot_log.info(f'user {callback.from_user.full_name} with id {callback.from_user.id} back to main menu')

        await callback.message.edit_text('Главное меню')
        await callback.message.edit_reply_markup(reply_markup=KeyboardManager.main_menu())
        await state.set_state(MenuStates.choosing_option)
