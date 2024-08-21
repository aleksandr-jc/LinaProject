# TODO зібрати інформацію з сайту https://youcontrol.com.ua/catalog/kved/58/11/ по кведу 58.1 видавнича справа, на кожну компанію

import requests
from bs4 import BeautifulSoup

def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }
    # робимо запит на сайт
    req = requests.get(url, headers=headers)

    # зберігаємо html сторінку з сайту локально
    # with open('data/youcontrol/youcontrol.html', 'w') as file:
    #     file.write(req.text)
    
    # працюємо з локальною html сторінкою сайту
    with open('data/youcontrol/youcontrol.html') as file:
        src = file.read()

    # створюємо обьєкт soup
    soup = BeautifulSoup(src, 'lxml')

    # виділяємо потрібну частину html
    block = soup.find('tbody')
    # знаходми частину коду з посиланням на видавництва
    articles = block.find_all('a', class_='link-details link-open')
    # список де будемо зберігати всі посилання
    project_urls = []
    # створюємо цикл для того щоб пройтись та збергіти всі посилання в правильній структурі
    for article in articles:
        project_url = 'https://youcontrol.com.ua' + article.get('href')
        project_urls.append(project_url)

    # збергіємо посилання в оркмому документі
    with open('data/youcontrol/publisher_links.txt', 'a') as file:
        for url in project_urls:
            file.write(f'{url}\n')


if __name__ == '__main__':
    base_url = 'https://youcontrol.com.ua/catalog/kved/58/11/'
    split = '/'

    for x in range(1, 144):
        url = f'{base_url}{x}{split}'
        print(f"Page: {x} ----------- {url}")
        get_data(url)
