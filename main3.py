import os
import xml.etree.ElementTree as ET
import json
import statistics

# Пути
input_dir = "data/3"  # Папка, содержащая XML-файлы
output_dir = "output/3"  # Папка для сохранения JSON и результатов

# Убедиться, что выходная папка существует
os.makedirs(output_dir, exist_ok=True)

# Функция для очистки строк
def clean_string(value):
    if isinstance(value, str):
        return value.strip()
    return value

# Обновление функции парсинга с учетом очистки
def parse_and_clean_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {
        "name": clean_string(root.findtext("name")),
        "constellation": clean_string(root.findtext("constellation")),
        "spectral_class": clean_string(root.findtext("spectral-class")),
        "radius": float(root.findtext("radius")),
        "rotation": float(root.findtext("rotation").split()[0]),
        "age": float(root.findtext("age").split()[0]),
        "distance": float(root.findtext("distance").split()[0]),
        "absolute_magnitude": float(root.findtext("absolute-magnitude").split()[0]),
    }

# Перепарсить данные с очисткой
data_cleaned = []
for file_name in os.listdir(input_dir):
    if file_name.endswith('.xml'):
        file_path = os.path.join(input_dir, file_name)
        data_cleaned.append(parse_and_clean_xml(file_path))

# Пересчитать все результаты
# Частота созвездий
constellation_counts_cleaned = {}
for entry in data_cleaned:
    constellation = entry['constellation']
    constellation_counts_cleaned[constellation] = constellation_counts_cleaned.get(constellation, 0) + 1

# Фильтрация по созвездию 'Весы'
filtered_by_constellation_cleaned = [entry for entry in data_cleaned if entry['constellation'] == 'Весы']

# Статистика по радиусам
radii_cleaned = [entry['radius'] for entry in data_cleaned]
radius_stats_cleaned = {
    "sum": sum(radii_cleaned),
    "min": min(radii_cleaned),
    "max": max(radii_cleaned),
    "mean": statistics.mean(radii_cleaned),
    "median": statistics.median(radii_cleaned),
}

# Сортировка по расстоянию
sorted_by_distance_cleaned = sorted(data_cleaned, key=lambda x: x['distance'])

# Сохранение очищенных результатов
with open(os.path.join(output_dir, 'stars_data_cleaned.json'), 'w', encoding='utf-8') as f:
    json.dump(data_cleaned, f, ensure_ascii=False, indent=4)

with open(os.path.join(output_dir, 'sorted_by_distance_cleaned.json'), 'w', encoding='utf-8') as f:
    json.dump(sorted_by_distance_cleaned, f, ensure_ascii=False, indent=4)

with open(os.path.join(output_dir, 'filtered_by_constellation_cleaned.json'), 'w', encoding='utf-8') as f:
    json.dump(filtered_by_constellation_cleaned, f, ensure_ascii=False, indent=4)

with open(os.path.join(output_dir, 'radius_stats_cleaned.json'), 'w', encoding='utf-8') as f:
    json.dump(radius_stats_cleaned, f, ensure_ascii=False, indent=4)

with open(os.path.join(output_dir, 'constellation_counts_cleaned.json'), 'w', encoding='utf-8') as f:
    json.dump(constellation_counts_cleaned, f, ensure_ascii=False, indent=4)

# Пути новых файлов для проверки
(os.path.join(output_dir, 'stars_data_cleaned.json'),
 os.path.join(output_dir, 'sorted_by_distance_cleaned.json'),
 os.path.join(output_dir, 'filtered_by_constellation_cleaned.json'),
 os.path.join(output_dir, 'radius_stats_cleaned.json'),
 os.path.join(output_dir, 'constellation_counts_cleaned.json'))
