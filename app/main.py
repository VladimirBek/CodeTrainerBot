import asyncio

from app.bot import BotServiceHandlers
from app.config import settings


async def main():
    bot = BotServiceHandlers(token=settings.BOT_TOKEN)
    await bot.start_bot()


if __name__ == '__main__':
    asyncio.run(main())
