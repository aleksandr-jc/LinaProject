import requests
from bs4 import BeautifulSoup
import json

def get_data(url):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }
    # робимо запит на сайт
    req = requests.get(url, headers=headers)

    # зберігаємо локально html сторінку з каталогом книжок
    with open('data/knigoland/main/knigoland_books.html', 'w') as file:
        file.write(req.text)

    # відкриваємо локально
    with open('data/knigoland/main/knigoland_books.html') as file:
        src = file.read()

    # створюємо обьєкт soup
    soup = BeautifulSoup(src, 'lxml')

    # знаходимо блоки коду з потрібноюнам інформацією
    articles = soup.find_all('div', class_='knl-catalog-item__card')

    # збергіаємо посилання на кожну книжку з сторінки
    project_urls = []

    # проходимось циклом та знаходимо посилааня на кожну книжку з сторінки
    for article in articles:
        project_url = 'https://knigoland.com.ua' + article.find('div', class_='pa-2').find('a').get('href') # https://knigoland.com.ua/profesii-maybutnogo-sandrin-puverro-item
        project_urls.append(project_url)

    # створюємо цикл щоб пройтись по кожному посиланні та збераємо інформацію

    # створюємо список де будемо зберігати інформацію прокнижки
    book_data_list = []

    for project_url in project_urls:
        try:
            # робимо запит на сторінку з книжкою
            req = requests.get(project_url, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')

            book_data = soup.find('div', class_='knl-product-card-characteristics')
            book_name_soup = soup.find('div', class_='d-flex align-center')

            # знаходимо назву книжки
            try:
                book_name = book_name_soup.find('h1', class_='knl-product-card__h1 my-2')
                book_name = book_name.text.strip()
            except Exception:
                book_name = None
            
            # знаходимо автора

        except Exception:
            break

def get_feature_text(soup, feature_name):
    try:
        first_div = soup.find('div', class_='knl-product-card-characteristics__name', string=lambda text: feature_name in text)
        if first_div:
            second_div = first_div.find_next('div', class_='d-flex align-center')
    except Exception:
        return None