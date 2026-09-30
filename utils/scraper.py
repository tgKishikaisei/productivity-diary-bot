import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_top_hackernews():
    url = "https://news.ycombinator.com/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    titles = soup.select(".titleline a")
    return [title.get_text() for title in titles[:5]] # топ 5

# print(get_top_hackernews())

# def get_usd_rate():
#     response = requests.get("https://api.exchangerate.host/latest?base=USD")
#     data = response.json()
#     print(data)
#     # return data["rates"]["USS"]
#
# get_usd_rate()




def remove_old_task(days: int = 7) -> int:
    """Удаляет задачи старше days дней у всех пользователей. Возвращает число удалённых.

    Чтение и атомарная запись идут через utils.storage.
    """
    from utils.storage import load_data, save_data

    data = load_data()
    today = datetime.now()
    removed = 0
    for user_id, tasks in data.items():
        kept = []
        for task in tasks:
            date_str = task.get("created") or task.get("date")
            try:
                too_old = date_str and (today - datetime.strptime(date_str, "%Y-%m-%d")).days > days
            except ValueError:
                too_old = False  # если формат даты сломан — задачу сохраняем
            if too_old:
                removed += 1
            else:
                kept.append(task)
        data[user_id] = kept
    if removed:
        save_data(data)
    return removed
