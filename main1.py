from bs4 import BeautifulSoup
import os
import json
import statistics
from collections import Counter

# Функция для парсинга данных из одного HTML-файла
def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        # Извлечение данных
        tournament_type = soup.find("span", text=lambda t: t and "Тип:" in t).text.split(":")[1].strip() if soup.find("span", text=lambda t: t and "Тип:" in t) else None
        title = soup.find("h1", {"class": "title"}).text.replace("Турнир:", "").strip() if soup.find("h1", {"class": "title"}) else None
        city = soup.find("p", {"class": "address-p"}).text.split("Город:")[1].split("Начало:")[0].strip() if soup.find("p", {"class": "address-p"}) else None
        rounds = int(soup.find("span", {"class": "count"}).text.replace("Количество туров:", "").strip()) if soup.find("span", {"class": "count"}) else None
        time_control = soup.find("span", {"class": "year"}).text.replace("Контроль времени:", "").strip() if soup.find("span", {"class": "year"}) else None
        min_rating = int(soup.find("span", text=lambda t: t and "Минимальный рейтинг" in t).text.split(":")[1].strip()) if soup.find("span", text=lambda t: t and "Минимальный рейтинг" in t) else None
        rating = float(soup.find("span", text=lambda t: t and "Рейтинг:" in t).text.split(":")[1].strip()) if soup.find("span", text=lambda t: t and "Рейтинг:" in t) else None
        views = int(soup.find("span", text=lambda t: t and "Просмотры:" in t).text.split(":")[1].strip()) if soup.find("span", text=lambda t: t and "Просмотры:" in t) else None
        
        return {
            "type": tournament_type,
            "title": title,
            "city": city,
            "rounds": rounds,
            "time_control": time_control,
            "min_rating": min_rating,
            "rating": rating,
            "views": views
        }

# Путь к папке с файлами
folder_path = "data/1"

# Парсинг всех файлов
data = []
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        file_path = os.path.join(folder_path, filename)
        data.append(parse_html_file(file_path))

# Сохранение в json
with open("output/1/tournaments.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Сортировка по полю "views" (Просмотры)
sorted_data = sorted(data, key=lambda x: x["views"], reverse=True)

# Фильтрация по минимальному рейтингу (например, >= 2300)
filtered_data = [item for item in data if item["min_rating"] and item["min_rating"] >= 2300]

# Статистика по "rating" (Рейтинг)
ratings = [item["rating"] for item in data if item["rating"] is not None]
stats = {
    "sum": sum(ratings),
    "min": min(ratings),
    "max": max(ratings),
    "mean": statistics.mean(ratings),
    "median": statistics.median(ratings)
}

# Частота текстовых меток по "type"
type_frequency = Counter(item["type"] for item in data if item["type"] is not None)

# Сохранение результатов
with open("output/1/sorted_tournaments.json", "w", encoding="utf-8") as json_file:
    json.dump(sorted_data, json_file, ensure_ascii=False, indent=4)

with open("output/1/filtered_tournaments.json", "w", encoding="utf-8") as json_file:
    json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)

with open("output/1/stats.json", "w", encoding="utf-8") as json_file:
    json.dump(stats, json_file, ensure_ascii=False, indent=4)

with open("output/1/type_frequency.json", "w", encoding="utf-8") as json_file:
    json.dump(type_frequency, json_file, ensure_ascii=False, indent=4)
