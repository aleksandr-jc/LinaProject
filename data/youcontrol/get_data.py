import requests
from bs4 import BeautifulSoup
import re

def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }
    # робимо запит на сайт
    req = requests.get(url, headers=headers)

    # збергіємо сторінку локально
    # with open('data/youcontrol/youcontrol_publisher.html', 'w') as file:
    #     file.write(req.text)
    
    # відкриваємо локально сторінку
    with open('data/youcontrol/youcontrol_publisher.html') as file:
        src = file.read()
    
    # стоврюємо обьєкт soup 
    soup = BeautifulSoup(src, 'lxml')

    articles = soup.find('div', class_='seo-table')

 # TODO як витянути інформацію з сторінки


if __name__ == '__main__':
    get_data('https://youcontrol.com.ua/catalog/company_details/19365425/')