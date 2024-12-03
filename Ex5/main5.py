import requests

# Указываем URL страницы
url = 'https://www.mkso.ru/normative/itog-proverok'

# Отправляем GET-запрос
response = requests.get(url)

# Проверяем статус код ответа
if response.status_code == 200:
    # Сохраняем HTML в файл
    with open('Ex5/output5/page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("HTML сохранен в файл 'page.html'")
else:
    print(f"Ошибка загрузки страницы: {response.status_code}")
