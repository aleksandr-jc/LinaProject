import requests
from bs4 import BeautifulSoup
"""
Треба зібрати всі назви видавництв
"""

def get_book_pub(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }

    # робимо запит на сайт
    response = requests.get(url, headers=headers)

    # викоритсовуємо декодер
    response.encoding = 'utf-8'

    # зберігаємо сторінку локально
    with open('data/yakaboo/yakaboo_publishers.html', 'w') as file:
        file.write(response.text)

    # відкриваємо сторінку локально
    with open('data/yakaboo/yakaboo_publishers.html') as file:
        src = file.read()
    
    soup = BeautifulSoup(src, 'lxml')

    # знаходимо блок коду з потрібною нам інформацією 
    articles = soup.find_all('li', class_='etm-list__list-item')

    # список де зберігатиметься всі посилання на видавців
    project_urls = []

    # проходимо циклом по всім видавцям та отримуємо посилааня на сторінку видавця
    for article in articles:
        project_url = 'https://www.yakaboo.ua' + article.find('a', class_='etm-list__list-item--link').get('href')
        project_urls.append(project_url)

    with open('data/yakaboo/new_parcing/data/publisher_links.text', 'a') as file:
        for link in project_urls:
            file.write(f"{link}\n")



print('Початок парсингу')


alf = ["Б", "В","Г","Ґ","Д","Е","Є","Ж","З","И","І","Ї","Й","К","Л","М","Н","О","П","Р","С","Т","У","Ф","Х","Ц","Ч","Ш","Щ","Ю","Я"]
base_url = 'https://www.yakaboo.ua/ua/book_publisher/view/all?letter='
for x in alf:
    try:
        url = f"{base_url}{x}"
        print(url)
        get_book_pub(url)
    except:
        print('Заверщення парсингу!')
        break