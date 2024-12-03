from bs4 import BeautifulSoup
import os
import json
import statistics

# Папки для данных и результатов
input_folder = "data/2"
output_folder = "output/2"
os.makedirs(output_folder, exist_ok=True)

# Получение списка всех HTML-файлов в папке
all_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".html")]

# Функция для парсинга 
def parse_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        products = []
        for item in soup.select(".product-item"):
            product = {}
            product["id"] = item.select_one(".add-to-favorite")["data-id"]
            
            # Извлечение диагонали и названия устройства
            name_text = item.select_one("span").text.strip()
            diagonal, name = name_text.split("\"", 1)
            product["diagonal"] = diagonal.strip() + "\""
            product["name"] = name.strip()
            
            # Удаляем символа рубля "₽"
            product["price"] = int(item.select_one("price").text.strip().replace("₽", "").replace(" ", ""))
            
            # Корректная обработка бонусов
            bonus_text = item.select_one("strong").text.strip()
            product["bonus"] = int("".join(filter(str.isdigit, bonus_text)))
            
            # Характеристики из списка
            for li in item.select("ul > li"):
                field = li["type"]
                value = li.text.strip()
                product[field] = value
            products.append(product)
        return products

# Сбор данных из всех файлов
all_data = []
for file_path in all_files:
    all_data.extend(parse_html(file_path))

# Сохранение собранных данных в json
output_json_path = os.path.join(output_folder, "data.json")
with open(output_json_path, "w", encoding="utf-8") as output_file:
    json.dump(all_data, output_file, ensure_ascii=False, indent=2)

# Выполнение операций с данными
# Сортировка по цене
sorted_data = sorted(all_data, key=lambda x: x["price"])

#Фильтрация по AMOLED-матрице
filtered_data = [item for item in all_data if item.get("matrix") == "AMOLED"]

# Статистика по цене
prices = [item["price"] for item in all_data]
price_stats = {
    "sum": sum(prices),
    "min": min(prices),
    "max": max(prices),
    "mean": statistics.mean(prices)
}

#Частота меток для матриц
matrix_counts = {}
for item in all_data:
    matrix = item.get("matrix", "Unknown")
    matrix_counts[matrix] = matrix_counts.get(matrix, 0) + 1

# Сохранение результатов
output_sorted_path = os.path.join(output_folder, "sorted_by_price.json")
output_filtered_path = os.path.join(output_folder, "filtered_amoled.json")
output_stats_path = os.path.join(output_folder, "price_stats.json")
output_matrix_path = os.path.join(output_folder, "matrix_counts.json")

with open(output_sorted_path, "w", encoding="utf-8") as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=2)

with open(output_filtered_path, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

with open(output_stats_path, "w", encoding="utf-8") as f:
    json.dump(price_stats, f, ensure_ascii=False, indent=2)

with open(output_matrix_path, "w", encoding="utf-8") as f:
    json.dump(matrix_counts, f, ensure_ascii=False, indent=2)

# Печать путей выходных файлов
print("Данные сохранены в:", output_json_path)
print("Отсортированные данные сохранены в:", output_sorted_path)
print("Отфильтрованные данные сохранены в:", output_filtered_path)
print("Статистика по ценам сохранена в:", output_stats_path)
print("Частота меток для матриц сохранена в:", output_matrix_path)
