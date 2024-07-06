import json
from bs4 import BeautifulSoup
import requests

def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }
    # робимо запит на сайт
    req = requests.get(url, headers=headers)

    # зберігаємо локально html сторінку з каталогом книжок
    with open('data/bookclub/ebooks/data/bookclub_ebooks.html', 'w') as file:
        file.write(req.text)

    # відкриваємо локально щоб неробити нагрузку на сайт
    with open('data/bookclub/ebooks/data/bookclub_ebooks.html') as file:
        src = file.read()
    
    # створюємо обьєкт soup
    soup = BeautifulSoup(src, 'lxml')

    # знаходимо блок коду з потрібною нам інформацією, з ссилками на книжки
    articles = soup.find_all('section', class_='book-inlist')
    
    # зберігаємо посилання на кожну книжку з сторінки
    project_urls = []

    # проходимо циклом та знаходимо посилааня на кожну книжку з сторінки
    for article in articles:
        project_url = "https://bookclub.ua" + article.find('div', class_='book-inlist-name').find('a').get('href')
        project_urls.append(project_url)

    
    # створюємо список де будемо зберігати інформацію про книжки
    book_data_list = []

    # створюємо цикл щоб пройтись по кожному посиланні та збераємо інформацію
    for project_url in project_urls:
        try:
            req = requests.get(project_url, headers=headers)
            
            soup = BeautifulSoup(req.text, 'lxml')

            book_data = soup.find('div', class_='proddopinfo')
            


            # Знаходимо назву книжки
            book_names = soup.find('article', class_='prd-m-info-block')
            book_name = book_names.find('h1')
            book_name = book_name.text.strip()

            # Знаходимо автора
            book_author = get_feature_text(book_data, 'Aвтор')

            # Знаходимо мову книжки
            book_language = get_feature_text(book_data, 'Мова')

            # Знаходимо рік видання
            pub_year = get_feature_text(book_data, 'Рік видання')

            # Знаходимо назву видавця
            book_publisher = get_feature_text(book_data, 'Видавництво')

            # Знаходимо ISBN 
            isbn = get_feature_text(book_data, 'ISBN')
         
            # знаходимо жанр
            book_genre_find = soup.find('div', id='bread_crumbs')
            book_genre = book_genre_find.find('section').get_text()[9:].strip().replace('\xa0', ' ').replace('»', '-') 


            # Відсутня інформація на сайті
            translator = None
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
        except Exception as _ex:
            print(_ex)
            break
        
    # зберігаємо список в json файл
    with open('data/bookclub/ebooks/data/bookclub_ebooks.json', 'a', encoding='utf-8') as file:
        json.dump(book_data_list, file, indent=4, ensure_ascii=False)
    
    print(f'Кількість книжок: {len(book_data_list)}')


def get_feature_text(soup, feature_name):
    try:
        div_1 = soup.find('div', class_='prd-attr-name', string=lambda text: feature_name in text)
        if div_1:
            div_2 = div_1.find_next_sibling('div', class_='prd-attr-descr')
            if div_2:
                return div_2.text.strip()
    except Exception as _ex:
        print(_ex)
        return None
    

print("Початок парсингу!")

base_url = 'https://bookclub.ua/catalog/e-books/?i='
listmode = '&listmode=2'
start_value = 0
step = 20
max_attempts = 29

for attempt in range(30):
    try:
        current_value = start_value + attempt * step
        url = f'{base_url}{current_value}{listmode}'
        print(f'Page: {current_value//10}')
        data = get_data(url)
    except Exception:
        print('Кінець парсингу')
        break