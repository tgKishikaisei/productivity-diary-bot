def log_action(user_id, message):
    from config import LOG_FILE
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"User {user_id}: {message}\n")

import logging
from config import LOG_WARNING_FILE

# Базавая настройка логгера
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s -  %(name)s - %(message)s",
#     filename=LOG_WARNING_FILE,
#     filemode="a",
#     encoding="utf-8"
# )

# Уровни логирования: DEBUG < INFO < WARNING < ERROR < CRITICAL
# logger_export = logging.getLogger("logger_export")
# tasks_logger = logging.getLogger("tasks_logger")
# storage_logger = logging.getLogger("storage_logger")

# Общая настройка
file_handler = logging.FileHandler(LOG_WARNING_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"
))

# Создаём логгеры
logger_export = logging.getLogger("logger_export")
tasks_logger = logging.getLogger("tasks_logger")
storage_logger = logging.getLogger("storage_logger")

# Устанавливаем уровень логирования (можно разный для каждого)
logger_export.setLevel(logging.DEBUG)
tasks_logger.setLevel(logging.DEBUG)
storage_logger.setLevel(logging.DEBUG)

# Добавляем один и тот же обработчик ко всем логгерам
for logger in [logger_export, tasks_logger, storage_logger]:
    if not logger.hasHandlers():  # чтобы не дублировать
        logger.addHandler(file_handler)

