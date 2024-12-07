from bs4 import BeautifulSoup
import json
import os
import statistics
from collections import Counter

# Пути к загруженным HTML-файлам
file_paths = [
    'Ex5/2nd_part/pages/page1.html',  
    'Ex5/2nd_part/pages/page2.html',   
]

# Разбираем файлы и извлекаем необходимые данные
parsed_data = []
for file_path in file_paths:
    with open(file_path, 'rb') as file:  # Открываем как бинарный файл, чтобы избежать проблем с кодировкой
        content = file.read().decode('utf-8', errors='ignore')  # Декодируем в UTF-8 с обработкой ошибок
        soup = BeautifulSoup(content, 'html.parser')
        items = soup.select('.uss_shop_list_view_item')  # Селектор для элементов товаров
        for item in items:
            name = item.select_one('.uss_shop_name a').get_text(strip=True)  # Извлекаем название
            producer = item.select_one('.uss_shop_producer').get_text(strip=True).replace("Производитель:", "").strip()  # Извлекаем производителя
            description = item.select_one('.uss_shop_description').get_text(separator=" ", strip=True)  # Извлекаем описание
            price_element = item.select_one('.actual_price .price_class')  # Ищем элемент с ценой
            price = float(price_element.get('data-clear-price')) if price_element else None  # Преобразуем цену в число

            parsed_data.append({
                "name": name,
                "producer": producer,
                "description": description,
                "price": price
            })

# Сортировка по цене
sorted_by_price = sorted(parsed_data, key=lambda x: x['price'] if x['price'] is not None else float('inf'))

# Фильтрация по производителю "Delta"
filtered_by_producer = [item for item in parsed_data if item['producer'] == "Delta"]

# Статистический анализ по ценам
prices = [item['price'] for item in parsed_data if item['price'] is not None]
price_statistics = {
    "min_price": min(prices),  # Минимальная цена
    "max_price": max(prices),  # Максимальная цена
    "average_price": statistics.mean(prices)  # Средняя цена
}

# Анализ частоты терминов в описаниях
all_descriptions = " ".join([item['description'] for item in parsed_data])
word_frequencies = Counter(all_descriptions.split())  # Подсчет частоты слов

# Папка для сохранения результатов
output_dir = "Ex5/2nd_part/output_data"  # Укажите директорию для сохранения результатов
os.makedirs(output_dir, exist_ok=True)

# Сохраняем данные в JSON-файлы
outputs = {
    "sorted_by_price": sorted_by_price,
    "filtered_by_producer": filtered_by_producer,
    "price_statistics": price_statistics,
    "word_frequencies": word_frequencies.most_common()
}

for key, data in outputs.items():
    with open(os.path.join(output_dir, f"{key}.json"), "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

print(f"Результаты сохранены в директорию: {output_dir}")
