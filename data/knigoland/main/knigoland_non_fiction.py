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
    with open('data/knigoland/main/knigoland_non_fiction.html', 'w') as file:
        file.write(req.text)

    # відкриваємо локально
    with open('data/knigoland/main/knigoland_non_fiction.html') as file:
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

    # створюємо список де будемо зберігати інформацію прокнижки
    book_data_list = []
    # створюємо цикл щоб пройтись по кожному посиланні та збераємо інформацію
    for project_url in project_urls:
        try:
            # робимо запит на сторінку з книжкою
            req = requests.get(project_url, headers=headers)
            
            soup = BeautifulSoup(req.text, 'lxml')

            # вибираємо блок з кодом html де збергіається інформація про книжки
            book_data = soup.find('div', class_='knl-product-card-characteristics')
                 
            # знаходимо назву книжки
            book_name_soup = soup.find('div', class_='knl-product-card__detail-info px-4 px-lg-0')
            try:
                book_name = book_name_soup.find('h1', class_='knl-product-card__h1 my-2')
                book_name = book_name.text.strip()
            except Exception:
                book_name = None


            # знаходимо автора
            book_author = get_feature_text(book_data, 'Автори')

            # знайти видавця
            book_publisher = get_feature_text(book_data, 'Видавництво')

            # знаходимо ISBN
            isbn = get_feature(book_data, 'ISBN')

            # знаходимо мову
            book_language = get_feature(book_data, 'Мова')

            # знаходимо рік видання
            pub_year = get_feature(book_data, 'Рік видання')
            

            # знаходимо жанр
            genre_soup = soup.find('ul', class_='v-breadcrumbs knl-breadcrumbs px-4 py-2 pa-lg-0 mx-0 my-2 theme--light')
            book_genre = get_genre(genre_soup)
            


            # Інформації якої немає на сайті
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

        except Exception:
            break   





      

             # зберігаємо список в json файл
    with open('data/knigoland/data/processed/knigoland_non_fiction.json', 'a', encoding='utf-8') as file:
        json.dump(book_data_list, file, indent=4, ensure_ascii=False)


def get_genre(soup):
    try:
            # Знаходимо всі елементи li з класом 'knl-breadcrumbs__item'
        li_tags = soup.find_all('li', class_='knl-breadcrumbs__item')
        
        # Перевіряємо, чи кількість елементів достатня
        if len(li_tags) < 2:
            return None
        
        # Отримуємо текст передостаннього елемента
        second_last_li = li_tags[-2].get_text(strip=True)
        
        return second_last_li
    except Exception:
        return None


def get_feature_text(soup, feature_name):
    # Find all characteristic items
    characteristics = soup.find_all('div', class_='knl-product-card-characteristics__item')
    
    for item in characteristics:
        name = item.find('div', class_='knl-product-card-characteristics__name')
        value = item.find('div', class_='knl-product-card-characteristics__value')
        
        if name and value and feature_name in name.text.strip():
            # Extract and return text from value
            return value.get_text(strip=True)
    
    return None


def get_feature(soup, feature_name):
    try:
        div_1 = soup.find('div', class_='knl-product-card-characteristics__name', string=lambda text: feature_name in text)
        if div_1:
            div_2 = div_1.find_next_sibling('div', class_='knl-product-card-characteristics__value').find('span')
            if div_2:
                return div_2.text
    except Exception:
        return None

# виклик на першу сторінку 
print(f'Початок парсингу!')
# get_data('https://knigoland.com.ua/non-fiction-')

# робимо цикл щоб пройтись по всім сторінкам
base_url = 'https://knigoland.com.ua/non-fiction-?PAGEN_1='


# зробив до 11 сторінки включно
start_value = 12
# встановлюємо кількість циклів всього 387 сторінок
max_attempts = 20

for attempt in range(max_attempts):
    try:
        url = f"{base_url}{start_value}"
        print(f'Page: {start_value}')
        data = get_data(url)
        start_value += 1
    except Exception as _ex:
        print(_ex)
        print('Заверщення парсингу')
        break
        