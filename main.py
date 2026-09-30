import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN, PARSE_MODE
from handlers.commands import commands_router
from handlers.tasks import tasks_router
from handlers.export import export_router

from utils.logger_aiogram import setup_logging
# Настройка Long polling
async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=PARSE_MODE))
    dp = Dispatcher()

    dp.include_router(router=tasks_router)
    dp.include_router(router=export_router)
    dp.include_router(router=commands_router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())

