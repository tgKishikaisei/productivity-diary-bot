"""Тесты без сети. Запуск: python -m pytest tests"""
import asyncio
import importlib
import json
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["DIARY_DATA_DIR"] = tempfile.mkdtemp()
os.environ["TELEGRAM_BOT_TOKEN"] = "123456:TEST"
os.environ["ADMIN_IDS"] = "1"

import config  # noqa: E402
from handlers import commands, export, tasks  # noqa: E402
from utils import storage  # noqa: E402


@pytest.fixture(autouse=True)
def clean_data():
    for f in Path(config.DATA_DIR).glob("tasks.json*"):
        f.unlink()
    yield


def msg(user_id=5):
    return SimpleNamespace(from_user=SimpleNamespace(id=user_id), answer=AsyncMock(), answer_document=AsyncMock())


def cmd(args):
    return SimpleNamespace(args=args)


def test_add_list_done():
    m = msg()
    asyncio.run(tasks.cmd_add(m, cmd("Купить <молоко>")))
    asyncio.run(tasks.cmd_add(m, cmd("Позвонить")))
    asyncio.run(tasks.cmd_list(m))
    assert "1. Купить &lt;молоко&gt;" in m.answer.await_args.args[0]
    asyncio.run(tasks.cmd_done(m, cmd("1")))
    assert storage.list_tasks(5) == ["Позвонить"]
    asyncio.run(tasks.cmd_done(m, cmd("9")))
    assert "Нет задачи" in m.answer.await_args.args[0]


def test_corrupted_file_is_not_overwritten():
    Path(config.TASK_FILE).write_text('{"1": [{"text": "чужая задача"', encoding="utf-8")
    m = msg()
    asyncio.run(tasks.cmd_add(m, cmd("новая")))
    assert "Ошибка" in m.answer.await_args.args[0]
    backups = list(Path(config.DATA_DIR).glob("tasks.json.corrupt-*"))
    assert len(backups) == 1 and "чужая задача" in backups[0].read_text(encoding="utf-8")


def test_export_is_in_memory():
    m = msg()
    storage.add_task(5, "задача")
    asyncio.run(export.cmd_export(m))
    document = m.answer_document.await_args.args[0]
    assert document.data.decode("utf-8") == "1. задача"
    assert not list(Path(config.DATA_DIR).glob("*_tasks.txt"))


def test_cleanup_only_for_admin_and_removes_old():
    data = {"5": [{"text": "old", "created": "2020-01-01"}, {"text": "new", "created": "2999-01-01"}]}
    Path(config.TASK_FILE).write_text(json.dumps(data), encoding="utf-8")
    stranger = msg(5)
    asyncio.run(commands.cleanup_command(stranger))
    assert storage.list_tasks(5) == ["old", "new"]
    admin = msg(1)
    asyncio.run(commands.cleanup_command(admin))
    assert storage.list_tasks(5) == ["new"] and "1" in admin.answer.await_args.args[0]
