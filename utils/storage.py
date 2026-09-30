"""Хранилище задач в JSON.

Битый tasks.json откладывается в копию, а запись отказывается перезаписывать данные,
поэтому задачи остальных пользователей не пропадут. Запись идёт через временный файл
и os.replace, сбой посреди записи не оставит обрезанный JSON.
"""
import json
import os
import tempfile
from datetime import datetime

from config import TASK_FILE
from utils.logger import storage_logger


class StorageError(Exception):
    """Файл задач повреждён или недоступен — данные не трогаем."""


def load_data() -> dict:
    if not os.path.exists(TASK_FILE):
        return {}
    try:
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
        data = json.loads(content) if content else {}
        if not isinstance(data, dict):
            raise ValueError("ожидался объект JSON")
        return data
    except (json.JSONDecodeError, ValueError) as error:
        backup = f"{TASK_FILE}.corrupt-{datetime.now():%Y%m%d-%H%M%S}"
        try:
            os.replace(TASK_FILE, backup)
        except OSError:
            pass
        storage_logger.error("Файл задач повреждён (%s), копия: %s", error, backup)
        raise StorageError("файл задач повреждён") from error
    except OSError as error:
        storage_logger.error("Не удалось прочитать файл задач: %s", error)
        raise StorageError("файл задач недоступен") from error


def save_data(data: dict) -> None:
    directory = os.path.dirname(TASK_FILE)
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".tasks-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, TASK_FILE)
    except BaseException:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def add_task(user_id, task: str) -> None:
    data = load_data()
    data.setdefault(str(user_id), []).append({"text": task, "created": datetime.now().strftime("%Y-%m-%d")})
    save_data(data)


def list_tasks(user_id) -> list[str]:
    return [t["text"] for t in load_data().get(str(user_id), [])]


def remove_task(user_id, number: int) -> str | None:
    """Удаляет задачу по номеру из /list (с 1). Возвращает её текст или None."""
    data = load_data()
    tasks = data.get(str(user_id), [])
    if not 1 <= number <= len(tasks):
        return None
    removed = tasks.pop(number - 1)
    save_data(data)
    return removed["text"]


def get_tasks_for_user(user_id) -> list[str]:
    return list_tasks(user_id)
