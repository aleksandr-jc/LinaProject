from bs4 import BeautifulSoup
import requests

def data(url):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }

    project_url = url

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
        

        book_data_list = []

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
        print(book_data_list)
    except Exception:
        print('END')
    


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

data(url='https://knigoland.com.ua/mistetstvo-spokusi-24-zakoni-perekonannya-item')