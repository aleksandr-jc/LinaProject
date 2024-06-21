import requests
from bs4 import BeautifulSoup
import json

def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }

    # робимо запрос на сайт
    req = requests.get(url, headers=headers)

    # зберігаємо локально сайт
    with open('data/readeat/main/readeat_books.html', 'w') as file:
        file.write(req.text)

    # відкриваємо локально сайт
    with open('data/readeat/main/readeat_books.html') as file:
        src = file.read()
    
    # створюжмо обьєкт soup та використовюємо парсер lxml
    soup = BeautifulSoup(src, 'lxml')

    # знаходимо блок html коду з потрібною нам інформацією 
    articles = soup.find_all('div', class_='col-6 col-sm-6 col-lg-4 col-xl-3')

    # зберігатемом тут всі ссилки на книжки
    project_urls = []

    for article in articles:
        project_url = article.find('div', class_='card-img-top position-relative px-3 px-md-0').find('a').get('href')
        project_urls.append(project_url)
    
    # створюємо циклд щоб пройтись по кожному url
    
    # створюємо пустий список де будемо збергігати інформацію про книжки 
    book_data_list = []

    for project_url in project_urls:
        # робимо запит по кожному url
        req = requests.get(project_url, headers=headers)

        # беремо назву з url для збереження файлів html по кожній книжці
        project_name = project_url.split('/')[-1]

        # зберігаємо локально кожний html книжок
        with open(f'data/readeat/data/raw/raw2/{project_name}.html', 'w') as file:
            file.write(req.text)
        
        # відкриваємо локально кожний html книжок
        with open(f'data/readeat/data/raw/raw2/{project_name}.html') as file:
            src = file.read()

        # стоврюмо обьєкт soup для парсингу кожної сторінки з книжкою
        soup = BeautifulSoup(src, 'lxml')
        book_data = soup.find('div', class_='container-xxl product-container mb-2 mb-lg-4')
        book_info = soup.find('div', class_='readmore')

        # пошук назви книжки
        try:
            book_name = book_data.find('h1', class_='mb-4 fs-2 pe-5') # mb-4 fs-2 pe-5
            book_name = book_name.text.strip()
        except Exception:
            book_name = None
        
        # знаходимо автора книжки
        try:
            book_author = book_data.find('a', class_='d-inline-block link-primary me-2')
            book_author = book_author.text.strip()
        except Exception:
            book_author = None
        
        # знаходимо видавництво
        book_publisher = get_feature_text(book_info, 'Видавництво')

        # знаходимо рік видання
        pub_year = get_feature_text(book_info, 'Рік видання')
  
        # знаходимо мову перекладу
        book_language = get_feature(book_info, 'Мова')
        
        # знаходимо перекладача
        translator = get_feature(book_info, 'Перекладач')

        # знаходимо оригінальну мову, але на сайті не має її 
        book_original_language = get_feature(book_info, 'Оригінальна мова')

        # знаходимо оригінальну назву книжки
        book_original_name = get_feature(book_info, 'Оригінальна назва')

        # знаходимо isbn
        isbn = get_feature(book_info, 'ISBN')

        # знаходимо жанр книги передаємо тут обьєк soup з кодом навігації сайту, звідси ми і візьмемо жанр
        book_genre_soup = soup.find('nav', attrs={'aria-label': 'breadcrumb'})
        book_genre = get_genre(book_genre_soup)

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

    # зберігаємо список в json файл
    with open('data/readeat/data/processed/readeat_json.json', 'a', encoding='utf-8') as file:
        json.dump(book_data_list, file, indent=4, ensure_ascii=False)

    print('---Done---')



# функція яка знаходить жанр книжки
def get_genre(soup):
    try:
        first_li = soup.find('li', class_='breadcrumb-item d-flex text-nowrap')

        if first_li:
            second_li = first_li.find_next('li', class_="breadcrumb-item d-flex text-nowrap")
            if second_li:
                third_li = second_li.find_next('li', class_='breadcrumb-item d-flex text-nowrap')
                if third_li:
                    return third_li.text.strip()
    except Exception:
        return None

# функція яка знаходить інформацію якщо вона є ссилкою
def get_feature_text(soup, feature_name):
    try:
        first_div = soup.find('span', class_='text-muted', string=lambda text: feature_name in text)
        if first_div:
            second_div = first_div.find_next('div', 'col-6 lh-sm')
            if second_div:
                a = second_div.find('a')
                if a:
                    return a.text.strip()
        return None
    except Exception:
        return None

# функція яка знаходить інформаію якщо вона не є ссилкою
def get_feature(soup, feature_name):
    try:
        first_div = soup.find('span', class_='text-muted', string=lambda text: feature_name in text)
        if first_div:
            second_div = first_div.find_next('div', 'col-6 lh-sm')
            if second_div:
                return second_div.text.strip()
        return None
    except Exception:
        return None

# виклик на першу сторінку 
print(f'Початок парсингу!')
# get_data(url='https://readeat.com/catalog/knigi')

# робимо цикл щоб пройтись по всім сторінкам
base_url = 'https://readeat.com/catalog/knigi?page='

# початкова сторінка
# зробив до 61 включно
# зробив до 141 включно
# зробив до 241 включно
start_value = 242
# встановлюємо кількість циклів всього 387 сторінок
max_attempts = 100

for attempt in range(max_attempts):
    try:
        url = f"{base_url}{start_value}"
        print(f'Page: {start_value}')
        data = get_data(url)
        start_value += 1
    except Exception as _ex:
        print(_ex)
        break