from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

from utils.logger import logger_export
from utils.storage import StorageError, get_tasks_for_user

export_router = Router(name="export_router")


@export_router.message(Command(commands=['export']))
async def cmd_export(message: Message):
    # Файл собирается в памяти (BufferedInputFile) и на диске не остаётся
    try:
        tasks = get_tasks_for_user(message.from_user.id)
    except StorageError:
        await message.answer("❌ Не удалось прочитать задачи. Попробуй позже.")
        return
    if not tasks:
        await message.answer("❓ У тебя нет задач для экспорта")
        return
    content = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(tasks)).encode("utf-8")
    await message.answer_document(BufferedInputFile(content, filename="tasks.txt"))
    logger_export.info("export for user %s: %s tasks", message.from_user.id, len(tasks))
