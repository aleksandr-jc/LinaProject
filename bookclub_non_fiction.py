import random
import time
import requests
from bs4 import BeautifulSoup
import json
"""
Витягуємо інформацію про книжки з сайту bookclub.ua зберігаємо в json файлі.
"""
def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }
    # робимо запит на сайт
    req = requests.get(url, headers=headers)

#    зберігаємо html сторінку локально
    with open('data/bookclub/non_fiction_books/main/bookclub.html', 'w') as file:
        file.write(req.text)

    # відкриваємо локальний файл html, щоб зробити меншу нагрузку на сайт
    with open('data/bookclub/non_fiction_books/main/bookclub.html') as file:
        src = file.read()
    
    # створюємо обьєкт soup 
    soup = BeautifulSoup(src, 'lxml')

    # знаходимо блок html коду з потрібною нам інформацією
    articles = soup.find_all('section', class_='book-inlist')

  
    project_urls = []         # створюємо список з url
    for article in articles:
        project_url = "https://bookclub.ua/" + article.find('div', class_='book-inlist-name').find('a').get('href')
        project_urls.append(project_url)
    
    # стоврюємо цикл щоб пройтись по кожному url
    book_data_list = []
    for project_url in project_urls:                   # зробимо зріз на одну книгу
        # робимо запит по кожному url 
        req = requests.get(project_url, headers=headers)
        # беремо назву з url
        project_name = project_url.split("/")[-1]

        with open(f'data/bookclub/non_fiction_books/data/{project_name}.html', 'w') as file:
            file.write(req.text)

        with open(f'data/bookclub/non_fiction_books/data/{project_name}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        book_data = soup.find('div', class_='prd-attributes')
        
        # знаходимо назву книжки
        try:        # блоки try/except будуть надавати значення None привідсутності даних
            book_name = book_data.find('div', class_='prd-attr-descr', itemprop='name')
            book_name = book_name.text.strip()
        except Exception:
            book_name = None

        # знаходимо автора книги
        try:
            book_author = book_data.find('div', class_='prd-attr-name', string="Автор ").find_next_sibling('div', class_='prd-attr-descr')
            book_author =book_author.text.strip()
        except Exception:
            book_author = None
        
        # знаходимо мову на якій написана книжка
        try:
            book_language = book_data.find('div', class_='prd-attr-name', string='Мова ').find_next_sibling('div', class_='prd-attr-descr')
            book_language = book_language.text.strip()
        except Exception:
            book_language = None
        
        # оригінальна назва книжки
        try:
            book_original_name = book_data.find('div', class_='prd-attr-name', string='Оригінальна назва ').find_next_sibling('div', class_='prd-attr-descr')
            book_original_name = book_original_name.text.strip()
        except Exception:
            book_original_name = None

        # оригнальна мова
        try:
            book_original_language = book_data.find('div', class_='prd-attr-name', string='Мова оригіналу ').find_next_sibling('div', class_='prd-attr-descr')
            book_original_language = book_original_language.text.strip()
        except Exception:
            book_original_language = None

        # знаходимо видавництво книжки
        try:
            book_publisher = book_data.find('div', class_='prd-attr-name', string='Видавництво ').find_next_sibling('div', class_='prd-attr-descr')
            book_publisher = book_publisher.text.strip()
        except Exception:
            book_publisher = None

        # знаходимо перекладача(ів) книжки
        try:
            translator = book_data.find('div', class_='prd-attr-name', string='Перекладач(і) ').find_next_sibling('div', class_='prd-attr-descr')
            translator = translator.text.strip()
        except Exception:
            translator = None
        
        # рік видання книжки
        try:
            pub_year = book_data.find('div', class_='prd-attr-name', string='Рік видання ').find_next_sibling('div', class_='prd-attr-descr')
            pub_year = pub_year.text.strip()
        except Exception:
            pub_year = None

        # ISBN
        try:
            isbn = book_data.find('div', class_='prd-attr-name', string='ISBN ').find_next_sibling('div', class_='prd-attr-descr')
            isbn = isbn.text.strip()
        except Exception:
            isbn = None
        
        # жанр книжки
        try:
            book_genre = book_data.find('div', class_='prd-attr-name', string='Розділ:  ').find_next_sibling('div', class_='prd-attr-descr').a
            book_genre = book_genre.text.strip()
        except Exception:
            book_genre = None

        book_data_list.append(
            {
                'Імʼя автора': book_author,
                'Назва книги': book_name,
                'Мова': book_language,
                'Мова оригіналу': book_original_language,
                'Оригінальна назва': book_original_name,
                'Назва видавця': book_publisher,
                'Рік видання': pub_year,
                'ISBN': isbn,
                'Жанр книги': book_genre,
            }
        )
    # print(book_data_list)
    time.sleep(random.randrange(2, 4))
    # зберігаємо список в json файлі
    with open('data/bookclub/non_fiction_books/main/bookclub_non_fiction.json', 'a', encoding='utf-8') as file:
        json.dump(book_data_list, file, indent=4, ensure_ascii=False)
    print('Done!')

# url = 'https://bookclub.ua/catalog/books/prikladni/?listmode=2'
# get_data(url)
         
base_url = 'https://bookclub.ua/catalog/books/prikladni/?i='
listmode = '&listmode=2'
start_value = 0
step = 20
max_attempts = 10000  # максимальна кількість ітерацій

for attempt in range(max_attempts):
    try:
        current_value = start_value + attempt * step
        url = f"{base_url}{current_value}{listmode}"
        print(f"Fetching data from: {url}")
        data = get_data(url)
        # Обробка отриманих даних
        # Наприклад, можна зберегти або обробити data
    except current_value == 540:
        print('!!!!!END!!!!!')
        break  # перервати цикл у випадку помилки