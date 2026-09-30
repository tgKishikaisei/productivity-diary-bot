import os
from dotenv import load_dotenv
from aiogram.enums import ParseMode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PARSE_MODE = ParseMode.HTML
# Пути от папки бота, чтобы задачи находились при запуске из любого каталога
DATA_DIR = os.environ.get("DIARY_DATA_DIR") or os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
TASK_FILE = os.path.join(DATA_DIR, "tasks.json")
LOG_FILE = os.path.join(DATA_DIR, "log.txt")
LOG_WARNING_FILE = os.path.join(DATA_DIR, "log_warning.txt")
LOG_WARNING_FILE_AIOGRAM = os.path.join(DATA_DIR, "aiogram_log.txt")
