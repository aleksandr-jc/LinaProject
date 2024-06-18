from bs4 import BeautifulSoup


with open(f'data/sens/data/den-koly-ya-potrapyla-u-kazku.html') as file:
            src = file.read()

soup = BeautifulSoup(src, 'lxml')

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

# Витягуємо автора та видавництво
author = get_feature_text(soup, 'Автор')
publisher = get_feature_text(soup, 'Видавництво')
ganre = get_feature_text(soup, 'Розділ')

print(f'Автор: {author}')
print(f'Видавництво: {publisher}')
print(f'Розділ: {ganre}')



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

# Витягуємо рік видання
publish_year = get_year(soup, 'Рік видання')
isbn = get_year(soup, ' Штрихкод')

print(f'Рік видання: {publish_year}')
print(f"ISBN: {isbn}")