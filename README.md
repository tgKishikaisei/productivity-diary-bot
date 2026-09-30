# Productivity Diary Bot

Дневник задач в Telegram. Команда `/add` записывает задачу, `/done` её закрывает, `/export` присылает весь список файлом. Задачи старше недели администратор чистит одной командой.

[![License](https://img.shields.io/github/license/tgKishikaisei/productivity-diary-bot)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/tgKishikaisei/productivity-diary-bot/ci.yml?branch=main&label=CI)](https://github.com/tgKishikaisei/productivity-diary-bot/actions/workflows/ci.yml)

## Команды

| Команда | Что делает |
|---|---|
| `/add текст` | новая задача |
| `/list` | ваши задачи с номерами |
| `/done номер` | отметить задачу выполненной и убрать из списка |
| `/export` | файл со всеми задачами, собранный в памяти |
| `/cleanup` | удалить задачи старше 7 дней у всех; работает только для `ADMIN_IDS` |

Задачи хранятся в `data/tasks.json`. Бот пишет файл атомарно и не теряет данные остальных пользователей, если файл повреждён: битая копия откладывается рядом.

## Стек

Python 3.12, aiogram 3.

## Запуск

```bash
git clone https://github.com/tgKishikaisei/productivity-diary-bot.git
cd productivity-diary-bot
python -m venv venv
venv\Scripts\activate               # Linux и macOS: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                 # TELEGRAM_BOT_TOKEN и ADMIN_IDS через запятую
python main.py
```

## Тесты

```bash
pip install pytest
python -m pytest -q
```

## Демо

Скриншотов нет: бот работает в Telegram, запустите его со своим токеном от @BotFather.

## Лицензия

[MIT](LICENSE) © 2026 Behruz Avezmatov
