import logging
from config import LOG_WARNING_FILE_AIOGRAM
# aiogram_logger = logging.getLogger("aiogram")
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s -  [aiogram] - %(message)s",
#     filename=LOG_WARNING_FILE_AIOGRAM,
#     filemode="a",
#     encoding="utf-8"
# )

# Получаем логгер aiogram
def setup_logging():
    loggers = [
        "aiogram",
        "aiogram.dispatcher",
        "aiogram.event",
        "aiogram.client"
    ]

    for name in loggers:
        logger = logging.getLogger(name)
        # DEBUG писал в файл каждое обновление целиком, включая тексты пользователей
        logger.setLevel(logging.INFO)

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        file_handler = logging.FileHandler(LOG_WARNING_FILE_AIOGRAM, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"
        ))

        logger.addHandler(file_handler)
