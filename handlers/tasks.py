from html import escape

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from utils.logger import log_action, tasks_logger
from utils.storage import StorageError, add_task, list_tasks, remove_task

tasks_router = Router(name='tasks_router')
MAX_TASK_LENGTH = 500


@tasks_router.message(Command(commands=["add"]))
async def cmd_add(message: Message, command: CommandObject):
    # Текст задачи берём из CommandObject: так работают и «/add@bot», и «/add» внутри текста
    task = (command.args or "").strip()
    if not task:
        await message.answer("❌ Напиши текст задачи после /add")
        return
    if len(task) > MAX_TASK_LENGTH:
        await message.answer(f"❌ Слишком длинная задача (максимум {MAX_TASK_LENGTH} символов)")
        return
    try:
        add_task(message.from_user.id, task)
    except (StorageError, OSError):
        tasks_logger.exception("add_task failed")
        await message.answer("🚫 Ошибка при добавлении задачи. Данные не изменены, попробуй позже.")
        return
    log_action(message.from_user.id, "добавлена задача")
    await message.answer(f"✅ Задача добавлена: {escape(task)}")  # бот работает с parse_mode=HTML


@tasks_router.message(Command(commands=["list"]))
async def cmd_list(message: Message):
    try:
        tasks = list_tasks(message.from_user.id)
    except StorageError:
        await message.answer("❌ Не удалось получить список задач")
        return
    if tasks:
        await message.answer("\n".join(f"{i + 1}. {escape(t)}" for i, t in enumerate(tasks))
                             + "\n\nВыполнил задачу? /done номер")
    else:
        await message.answer("❓ У тебя нет задач")


@tasks_router.message(Command(commands=["done"]))
async def cmd_done(message: Message, command: CommandObject):
    arg = (command.args or "").strip()
    if not arg.isdigit():
        await message.answer("❌ Укажи номер задачи из /list, например: /done 2")
        return
    try:
        removed = remove_task(message.from_user.id, int(arg))
    except StorageError:
        await message.answer("❌ Не удалось изменить список задач")
        return
    if removed is None:
        await message.answer("❌ Нет задачи с таким номером")
        return
    log_action(message.from_user.id, "задача выполнена")
    await message.answer(f"🎉 Выполнено: {escape(removed)}")
