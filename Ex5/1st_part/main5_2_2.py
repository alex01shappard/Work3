from bs4 import BeautifulSoup
import json
import os
import statistics
import chardet

# Функция для определения кодировки файла
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Директория с файлами
input_dir = "Ex5/1st_part/output5/10_pages"
parsed_data = []

# Получаем список всех html файлов 
files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.html')]

# Парсинг каждого файла
for file in files:
    # Определение кодировки
    encoding = detect_encoding(file)
    with open(file, 'r', encoding=encoding) as f:
        soup = BeautifulSoup(f, 'html.parser')

        # Извлечение данных
        product_data = {}
        product_data['name'] = soup.find('h1').get_text(strip=True) if soup.find('h1') else None
        price_tag = soup.find(class_='price_class')
        product_data['price'] = int(price_tag.get('data-clear-price')) if price_tag else None
        product_data['capacity'] = soup.find(text='Ёмкость').find_next('div').get_text(strip=True) if soup.find(text='Ёмкость') else None
        product_data['lifetime'] = soup.find(text='Срок службы').find_next('div').get_text(strip=True) if soup.find(text='Срок службы') else None
        dimensions = soup.find(text='Размеры (ДxШxВ)').find_next('div').get_text(strip=True) if soup.find(text='Размеры (ДxШxВ)') else None
        if dimensions:
            product_data['dimensions'] = dimensions
        product_data['weight'] = soup.find(text='Вес').find_next('div').get_text(strip=True) if soup.find(text='Вес') else None
        material = soup.find(text='Материал корпуса').find_next('div').get_text(strip=True) if soup.find(text='Материал корпуса') else None
        if material:
            product_data['material'] = material

        parsed_data.append(product_data)

# Сохранение результатов 
output_dir = "Ex5/1st_part/output5/output_data"
os.makedirs(output_dir, exist_ok=True)
parsed_data_path = os.path.join(output_dir, "parsed_data.json")

with open(parsed_data_path, 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=4)

# Операции с данными
# Сортировка по цене
sorted_by_price = sorted(parsed_data, key=lambda x: x['price'] if x['price'] else float('inf'))

# Фильтрация по ёмкости (например, содержит '24')
filtered_by_capacity = [item for item in parsed_data if '24' in (item.get('capacity') or '')]

# Статистика по цене
prices = [item['price'] for item in parsed_data if item['price'] is not None]
price_stats = {
    "min_price": min(prices),
    "max_price": max(prices),
    "mean_price": statistics.mean(prices)
}

# Частота материалов корпуса
material_counts = {}
for item in parsed_data:
    material = item.get('material')
    if material:
        material_counts[material] = material_counts.get(material, 0) + 1

# Сохранение результатов в json
sorted_data_path = os.path.join(output_dir, "sorted_by_price.json")
filtered_data_path = os.path.join(output_dir, "filtered_by_capacity.json")
stats_data_path = os.path.join(output_dir, "price_statistics.json")
frequency_data_path = os.path.join(output_dir, "material_frequency.json")

with open(sorted_data_path, 'w', encoding='utf-8') as f:
    json.dump(sorted_by_price, f, ensure_ascii=False, indent=4)

with open(filtered_data_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_by_capacity, f, ensure_ascii=False, indent=4)

with open(stats_data_path, 'w', encoding='utf-8') as f:
    json.dump(price_stats, f, ensure_ascii=False, indent=4)

with open(frequency_data_path, 'w', encoding='utf-8') as f:
    json.dump(material_counts, f, ensure_ascii=False, indent=4)

print("Данные успешно обработаны и сохранены.")
