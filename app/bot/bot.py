from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation

from logs import logger


class BotServiceHandlers:
    __slots__ = "token", "dp", "bot", "polling_manager", "request_manager"

    def __init__(self, token: str):
        # инициализируем root-бота и диспатчер
        bot = Bot(token=token)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())
        self.dp = dp
        self.bot = bot
        UserHandler(self.dp).register_handlers()


    async def start_root_bot(self):
        """Запуск бот сервисов. Запускает поллинг всех переданных ботов."""

        bot_name = await self.bot.me()
        logger.info(f"Lunching bot: {self.bot.id} - {bot_name.full_name} ")

        await self.dp.start_polling(self.bot, dp_for_new_bot=self.dp, polling_manager=self.polling_manager,
                                    request_manager=self.request_manager)


