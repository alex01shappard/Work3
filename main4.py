import os
import json
import xml.etree.ElementTree as ET
import statistics

# Путь к папкам 
input_folder = "data/4"
output_folder = "output/4"

os.makedirs(output_folder, exist_ok=True)

# Функция для парсинга XML 
def parse_xml_file(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    clothing_items = []
    for clothing in root.findall('clothing'):
        item = {}
        for attribute in clothing:
            item[attribute.tag] = attribute.text.strip() if attribute.text else None
        clothing_items.append(item)
    return clothing_items

xml_files = [os.path.join(input_folder, fname) for fname in ["1.xml", "2.xml"]]

# Парсинг данных из всех XML файлов
all_data = []
for xml_file in xml_files:
    all_data.extend(parse_xml_file(xml_file))

# Сохранение всех данных в json
all_data_json_path = os.path.join(output_folder, "all_data.json")
with open(all_data_json_path, "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

# Операции с данными
# Сортировка по полю "price"
sorted_data = sorted(all_data, key=lambda x: float(x.get("price", 0)))

#Фильтрация по полю "color" == "Зеленый"
filtered_data = [item for item in all_data if item.get("color") == "Зеленый"]

#Статистика для поля "rating"
ratings = [float(item["rating"]) for item in all_data if "rating" in item and item["rating"]]
rating_stats = {
    "sum": sum(ratings),
    "min": min(ratings),
    "max": max(ratings),
    "mean": statistics.mean(ratings),
    "median": statistics.median(ratings),
    "stdev": statistics.stdev(ratings) if len(ratings) > 1 else 0
}

#Частота текстовых меток в поле "category"
from collections import Counter
category_counts = Counter(item["category"] for item in all_data if "category" in item and item["category"])

# Сохранение результатов
sorted_data_json_path = os.path.join(output_folder, "sorted_data.json")
filtered_data_json_path = os.path.join(output_folder, "filtered_data.json")
stats_json_path = os.path.join(output_folder, "rating_stats.json")
category_counts_json_path = os.path.join(output_folder, "category_counts.json")

with open(sorted_data_json_path, "w", encoding="utf-8") as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=4)
with open(filtered_data_json_path, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)
with open(stats_json_path, "w", encoding="utf-8") as f:
    json.dump(rating_stats, f, ensure_ascii=False, indent=4)
with open(category_counts_json_path, "w", encoding="utf-8") as f:
    json.dump(category_counts, f, ensure_ascii=False, indent=4)

all_data_json_path, sorted_data_json_path, filtered_data_json_path, stats_json_path, category_counts_json_path
