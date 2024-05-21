from urllib.request import urlopen
from bs4 import BeautifulSoup

with open('/Users/oleksandrrobu/LinaProject/view-page-source.com-www.yakaboo.ua_ua_knigi_hudozhestvennaja-literatura.html?book_publication=Bumazhnaja.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

find_all_names = soup.find_all('a', class_='ui-card-title category-card__name')
book_titles = []

for name in find_all_names:
    book_titles.append(name.get('title'))

print(book_titles)
