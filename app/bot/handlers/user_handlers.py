from aiogram import Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.bot.keyboards import KeyboardManager
from app.bot.states.menu_states import MenuStates
from app.cruds.crud_category import crud_category
from app.cruds.crud_excercise import crud_exercise
from app.cruds.crud_level import crud_level
from app.db import LocalSession
from app.logs import logger


class UserHandler:
    __slots__ = "dp", "router"
    difficult_choose = None

    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.router = Router()
        self.dp.include_router(self.router)

    async def register_handlers(self):
        logger.info("Register user handlers")

        # Логика проверки почты в таблице
        self.router.message.register(self.start, Command('start'))

        self.router.callback_query.register(self.back_to_main_menu, F.data == 'back-to-main-menu')
        self.router.callback_query.register(self.get_instructions, F.data == 'get-instructions')
        self.router.message.register(self.get_task, Command('get_task'))
        async with LocalSession() as db:
            tasks = await crud_exercise.get_all(db)
            for task in tasks:
                self.router.callback_query.register(self.choose_task, F.data == str(task.id))

    async def start(self, message: Message, state: FSMContext):
        """ Хэндлер для команды старт """
        logger.info(
            f"START Handler {message.chat.id}  {message.from_user.username} {message.text}")

        text = "Главное меню. Допбро пожаловать!"
        await message.answer(text=text, reply_markup=KeyboardManager.main_menu())
        await state.set_state(MenuStates.choosing_option)

    async def get_instructions(self, callback: CallbackQuery, state: FSMContext):
        async with LocalSession() as db:
            levels = await crud_level.get_all(db)
            levels = [str(level.difficult) for level in levels]
            categoties = await crud_category.get_all(db)
            categories = [category.name for category in categoties]
        text = (f"Список доступных уровней сложности:\n\n{', '.join(levels)}\n\n"
                f"Список доступных тем:\n\n{', '.join(categories)}")
        await callback.message.answer(text)
        text = "Инструкция по использованию бота\nКоманда для получения заданий: /get_task <сложность> <тема>"
        await callback.message.answer(text)
        await callback.message.answer(text="Вернуться в главное меню",
                                      reply_markup=KeyboardManager().back_to_main_menu())

    async def get_task(self, message: Message, command: CommandObject, state: FSMContext) -> None:
        if command.args is None:
            await message.answer('Использование: /get_task <сложность> <тема>')
            return
        args = command.args.split()
        if len(args) != 2:
            await message.answer('Использование: /get_task <сложность> <тема>')
            return
        difficulty = args[0]
        topic = args[1]
        async with LocalSession() as db:
            topic_info = await crud_category.get_by_name(db, name=topic)
            if not topic_info:
                await message.answer('Тема не найдена')
                return
            topic_id = topic_info.id
            level_info = await crud_level.get_by_level(db, difficult=int(difficulty.strip()))
            if not level_info:
                await message.answer('Уровень сложности не найден')
                return
            level_id = level_info.id
            tasks = await crud_exercise.get_by_difficulty_and_topic(db, difficulty=level_id, topic_id=topic_id)
            if not tasks:
                await message.answer('Задания на данную темы с выбранным уровнем сложности не найдены')
                await message.answer('Использование: /get_task <сложность> <тема>')
                return
            try:
                for task in tasks[:11]:
                    await message.answer(text=task.name, reply_markup=KeyboardManager.tasks(task))
            except IndexError:
                for task in tasks:
                    await message.answer(text=task.name, reply_markup=KeyboardManager.tasks(task))

    async def choose_task(self, callback: CallbackQuery, state: FSMContext):
        async with LocalSession() as db:
            task = await crud_exercise.get(db, id=int(callback.data))
            await callback.message.edit_text(task.task)
            await callback.message.answer(text="Вернуться в главное меню",
                                          reply_markup=KeyboardManager().back_to_main_menu())

    async def back_to_main_menu(self, callback: CallbackQuery, state: FSMContext):
        logger.info(f'user {callback.from_user.full_name} with id {callback.from_user.id} back to main menu')

        await callback.message.edit_text('Главное меню')
        await callback.message.edit_reply_markup(reply_markup=KeyboardManager.main_menu())
        await state.set_state(MenuStates.choosing_option)
