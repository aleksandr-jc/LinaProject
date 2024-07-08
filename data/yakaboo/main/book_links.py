import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }
    # робимо запит на сайт
    response = requests.get(url, headers=headers)
    
    # використовуємо декодер
    response.encoding = 'utf-8'

    # зберігаємо сторінку локально
    with open('data/yakaboo/yakaboo.html', 'w') as file:
        file.write(response.text)
    
    # відкриваємо локально файл html. щою робити меншу нагрузку на сайт
    with open('data/yakaboo/yakaboo.html') as file:
        src = file.read()

    # стоврюємо обьєкт soup
    soup = BeautifulSoup(src, 'lxml')

    # знаходимо блок коду з потрібною нам інформацією
    articles = soup.find_all('div', class_='category-card category-layout')

    # список де зберігатиметься всі послиання на книжки
    project_urls = []


    # проходимось циклом по всім книжкам та отримуємо посилання на сторінку з книжкою 
    for article in articles:
        project_url = 'https://www.yakaboo.ua' + article.find('a', class_='category-card__image').get('href')
        project_urls.append(project_url)

    with open('data/yakaboo/main/book_links.txt', 'a') as file:
        for link in project_urls:
            file.write(f"{link}\n")


print("Початок парсингу!")
print('Page: 1')
get_data(url="https://www.yakaboo.ua/ua/knigi/hudozhestvennaja-literatura.html?book_publication=Bumazhnaja")

base_url = 'https://www.yakaboo.ua/ua/knigi/hudozhestvennaja-literatura.html?book_publication=Bumazhnaja&p='

for x in range(2, 11):    # 2049
    try:
        url = f"{base_url}{x}"
        print(f'Page: {x}')
        data = get_data(url)

    except Exception as _ex:
        print(_ex)
        print('Заверщення парсингу!')
        break