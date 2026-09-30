from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart,Command
import os

from utils.scraper import remove_old_task
from utils.storage import StorageError


def _admin_ids() -> set[int]:
    return {int(x) for x in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",") if x.isdigit()}

commands_router = Router(name='command_router')
# command_router.message(CommandStart)
@commands_router.message(Command(commands=["start"]))
async def start_command(message: Message):
    await message.answer("Привет! Это твой бот-дневник продуктивности. Используй /add чтобы добавить задачу, /list чтобы посмотреть их, /done номер — отметить выполненной и /export — выгрузить")

@commands_router.message(Command(commands=["cleanup"]))
async def cleanup_command(message: Message):
    # Очистка затрагивает задачи ВСЕХ пользователей, поэтому только для ADMIN_IDS.
    if message.from_user is None or message.from_user.id not in _admin_ids():
        await message.answer("⛔ Команда доступна только администратору.")
        return
    try:
        removed = remove_old_task(7)
    except StorageError:
        await message.answer("❌ Файл задач повреждён, очистка не выполнена.")
        return
    await message.answer(f"🧹 Удалено старых задач (7+ дней): {removed}")