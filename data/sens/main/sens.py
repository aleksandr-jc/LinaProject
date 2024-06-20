import requests
import re
import time
from bs4 import BeautifulSoup
import json


def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }
    # робимо запит на сайт
    req = requests.get(url, headers=headers)

#    зберігаємо html сторінку локально
    with open('data/sens/main/sens_books.html', 'w') as file:
        file.write(req.text)

    # відкриваємо локальний файл html, щоб зробити меншу нагрузку на сайт
    with open('data/sens/main/sens_books.html') as file:
        src = file.read()
    
    # створюємо обьєкт soup 
    soup = BeautifulSoup(src, 'lxml')

    # знаходимо блок html коду з потрібною нам інформацією
    articles = soup.find_all('li', class_='catalog-grid__item')

    project_urls = []

    for article in articles:
        project_url = "https://sens.in.ua" + article.find('div', class_='catalogCard-view').find('a').get('href')
        project_urls.append(project_url)
    
       # стоврюємо цикл щоб пройтись по кожному url
    book_data_list = []
    for project_url in project_urls:                   # зробимо зріз на одну книгу
        # робимо запит по кожному url 
        req = requests.get(project_url, headers=headers)
        # беремо назву з url
        project_name = project_url.split("/")[-2]

        # зберігаємо локально кожний html книжки
        with open(f'data/sens/data/{project_name}.html', 'w') as file:
            file.write(req.text)

        # відкриваємо локально кожни html книжки
        with open(f'data/sens/data/{project_name}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        book_data_name = soup.find('section', class_='product') # для пошуку назви книги

        book_data = soup.find('div', class_='product-features') # для пошуку інформації про книгу (автор, ісбн, видавництво, рік)
        
        # знаходимо назву книжки
        try:
            book_name = book_data_name.find('div', class_='product-header__block product-header__block--wide')
            book_name = book_name.text.strip()
            book_name = re.sub(r'\.\s*[^.]+$', '.', book_name)           
        except Exception:
            book_name = None
        
        # знаходимо автора книги
        book_author = get_feature_text(book_data, 'Автор')
        
        # знаходим видавництво
        book_publisher = get_feature_text(book_data, 'Видавництво')

        # знаходимо жанр
        book_genre = get_feature_text(book_data, 'Розділ')

        # знаходимо рік видання 
        pub_year = get_year(book_data, 'Рік видання')

        # знаходимо ISBN
        isbn = get_year(book_data, 'Штрихкод')

        # знаходимо перекладача
        translator = get_feature_text(book_data, 'Перекладач')

        # Інформація яка відсутня на сайті
        book_language = None   
        book_original_language = None
        book_original_name = None

        book_data_list.append(
            {
                'Імʼя автора': book_author,
                'Назва книги': book_name,
                'Мова': book_language,
                'Перекладач': translator,
                'Мова оригіналу': book_original_language,
                'Оригінальна назва': book_original_name,
                'Назва видавця': book_publisher,
                'Рік видання': pub_year,
                'ISBN': isbn,
                'Жанр книги': book_genre,
            }
        )          

    # Зберігаємо список в json файл
    with open('data/sens/main/sens_json.json', 'a', encoding='utf-8') as file:
        json.dump(book_data_list, file, indent=4, ensure_ascii=False)
    print('Done')

    time.sleep(2)

# Функція для витягнення тексту з комірки таблиці (Автор, видавництво, розділ)
def get_feature_text(soup, feature_name):          
    try:
        th = soup.find('th', class_='product-features__cell product-features__cell--h', string=lambda text: feature_name in text)
        if th:
            td = th.find_next_sibling('td', class_='product-features__cell')
            if td:
                a = td.find('a')
                if a:
                    return a.text.strip()
        return None
    except Exception as e:
        return None

# Функція для витягнення тексту з комірки таблиці (Рік видання, ISBN)
def get_year(soup, feature_name):
    try:
        th = soup.find('th', class_='product-features__cell product-features__cell--h', string=lambda text: feature_name in text)
        if th:
            td = th.find_next_sibling('td', class_='product-features__cell')
            if td:
                return td.text.strip()
        return None
    except Exception as e:
        return None


# виклик функції на першу сторінку
# get_data('https://sens.in.ua/kataloh/')
# зібрав перші 101 сторінку
# зібрав перші 302 сторінки
base_url = 'https://sens.in.ua/kataloh/filter/page='
listmode = '/'
start_value = 303
max_value = 101

for attempt in range(max_value):
    try:    
        url = f"{base_url}{start_value}{listmode}"
        print(f'Page {start_value}')
        data = get_data(url)
        start_value += 1 

    except Exception as _ex:
        print(_ex)
        print('END!')
        break