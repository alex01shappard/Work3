from bs4 import BeautifulSoup

# Открываем скачанный HTML-файл с правильной кодировкой
with open('Ex5/output5/page.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Извлекаем заголовок страницы (название товара)
title = soup.find('title').text
print(title)


