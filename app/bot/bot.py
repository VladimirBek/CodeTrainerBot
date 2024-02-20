from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation

from app.logs import logger

from app.bot.handlers import UserHandler


class BotServiceHandlers:
    __slots__ = "token", "dp", "bot"

    def __init__(self, token: str):
        bot = Bot(token=token)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())
        self.dp = dp
        self.bot = bot

    async def start_bot(self):
        """Запуск бот сервисов. Запускает поллинг всех переданных ботов."""

        bot_name = await self.bot.me()
        logger.info(f"Запуск бот сервиса id: {self.bot.id} - {bot_name.full_name} ")
        await UserHandler(self.dp).register_handlers()
        await self.dp.start_polling(self.bot)


