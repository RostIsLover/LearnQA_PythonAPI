import requests
from bs4 import BeautifulSoup

get_secret_password_homework_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_auth_cookie_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
wiki_url = 'https://en.wikipedia.org/wiki/List_of_the_most_common_passwords'
text_not_authorized = "You are NOT authorized"
login = "super_admin"
password = ""
payload = {}
cookies = {}

# Запрос в Википедию. Получаем html-страницу с 25 самыми популярными паролями
html_text = requests.get(wiki_url).text
soup = BeautifulSoup(html_text, 'html.parser')

# Парсим страницу. Перебираем все пароли по очереди
for password_from_wiki in soup.find_all("td", {"align": "left"}):

    # После парсинга пароли имеют на конце \n. Обрезаем его.
    password = password_from_wiki.text.replace("\n", "")

    # Составляем тело запроса для запроса токена
    payload.update({"login": login, "password": password})

    # Запрос на получение токена
    responseRegister = requests.post(get_secret_password_homework_url, payload)

    # Записываем полученный токен
    cookie_value = responseRegister.cookies.get('auth_cookie')

    # Если токен получен, то составляем куки для отправки следующего запроса
    if cookie_value is not None:
        cookies.update({'auth_cookie': cookie_value})

    # Запрос на проверку верного пароля
    responseCheckAuth = requests.get(check_auth_cookie_url, cookies=cookies)

    # Если пароль верный, то выведем пароль и фразу ответа
    if responseCheckAuth.text != text_not_authorized:
        print(f"Правильный пароль: {password}")
        print(f"Фраза: {responseCheckAuth.text}")
        break


