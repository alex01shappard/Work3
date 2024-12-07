import requests
import os

# Список страниц
urls = [
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-24/',
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-33/',
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-40/',
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-65/',
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-75/',
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-100/',
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-120/',
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-150/',
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-200/',
    'https://stvs.pro/store/akkumulyatornye-batarei-delta-dtm-l/akkumulyatornye-batarei-delta/akkumulyatornye-batarei-delta-seriya-gx-gel/akkumulyator-delta-gx-12-230/'
        
]

# Папка для сохранения
output_folder = 'Ex5/1st_part/output5/10_pages'

# Создаём папку, если её нет
os.makedirs(output_folder, exist_ok=True)

# Обрабатываем каждый URL
for i, url in enumerate(urls, start=1):
    try:
        # Отправляем GET-запрос
        response = requests.get(url)

        # Проверяем статус код ответа
        if response.status_code == 200:
            # Формируем имя файла
            file_path = os.path.join(output_folder, f'page{i}.html')

            # Сохраняем HTML в файл
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"html сохранен в файл '{file_path}'")
        else:
            print(f"Ошибка загрузки страницы {url}: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")

