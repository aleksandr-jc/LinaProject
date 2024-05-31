import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import json

def get_source_html(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    book_info = []

    try:
        driver.get(url=url)

        time.sleep(5)

        # Вибір опції "Рік видання" в селекторі
        search_type_select = Select(driver.find_element(By.NAME, "S21P03"))
        search_type_select.select_by_value("G=")
                
         # Введення року видання
        year_input = driver.find_element(By.NAME, "S21STR")  
        year_input.send_keys("2023")

        # Надсилання форми
        search_button = driver.find_element(By.NAME, "C21COM1")  
        search_button.click()

        start_value = 21
        step = 20

        time.sleep(3)

        while start_value != 7941:                # Контролюємо кількість ітерацій для тестів
            try:
                # Очікування завантаження результатів
                time.sleep(3)

                # Отримання результатів    
                main_content = driver.find_element(By.CLASS_NAME, 'advanced')
                results = main_content.find_elements(By.XPATH, "//td[@width='95%']")

                for result in results:
                    book_info.append(result.text.strip())
                                
                time.sleep(3)
                
                 # Формування значення для атрибуту value
                value = str(start_value)
                
                # Пошук елемента за його значенням value і клікаємо на нього
                button = driver.find_element(By.XPATH, f"//input[@type='submit' and @value='{value}']")
                button.click()
                
                # Чекати кілька секунд, щоб сторінка завантажилась (при необхідності)
                time.sleep(3)
                
                # Збільшення значення для наступного циклу
                start_value += step
            
            except Exception as e:
                print(f'Помилка: {e}')
                # break
            
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

    for book in book_info:
        book_info_parc(book)

def book_info_parc(book):
    # Форматуємо інформацію для кращого зчитання
    lines = book.split('\n')
    try:
        info = lines[2]
    except Exception:
        info = lines
# ім'я автора   
    try:
        author = lines[1].replace(',', '').replace('.', ' ')
    except Exception:
        author = ''
# назва книги
    try:
        title_match = re.search(r'(.*?)(?=\[Текст\])', info)
        title = title_match.group().strip() if title_match else ""  
    except Exception: 
        title = book
# жанр книги
    try:
        pattern = r' : \[?(.*?)\]? / '
        match = re.search(pattern, info).group(1)
        if len(match) < 30:
            ganre = match
        else: 
            ganre = ''
    except Exception:
        ganre = ''
 # видавництво       
    try:
        publisher_match = re.search(r'([А-ЯІЇЄҐ][а-яіїєґ]+ : [^,]+)', info)
        publisher = publisher_match.group().strip() 
    except Exception:
        publisher = ""  
# рік видачі    
    try:
        year_match = re.search(r"(\d{4})\.", info)
        year = year_match.group().replace('.', '').strip() 
    except Exception:
        year = "2023"  
# кількість примірників
    try: 
        copies_match = re.search(r"(\d+)\sприм\.", info)
        copies = copies_match.group(1).strip()
    except Exception:
        copies = ""  
# ISBN    
    try:
        isbn_match = re.search(r"ISBN\s(\d+-\d+-\d+-\d+-\d?)", info)
        isbn = isbn_match.group(1).strip() 
    except Exception:
        isbn = ""  

# Пошук перекладачів
    try:
       translators_match = re.search(r';\s(\[?пер\..*?\]?\.\s-)', info)
       translators = translators_match.group(1).strip()
    except Exception:
        translators = ''

    # зберігаю в json файлі
    book_list = []
    book_list.append(
        {
            "Ім'я автора": author.strip(),
            "Назва книги": title,
            "Жанр": ganre,
            "Видавництво": publisher,
            "Рік видачі": year,
            "Кількість примірників": copies,
            "ISBN": isbn,
            "Перекладач(і)": translators,            
        },
    )

    with open('data/nbuv/2023/main/nbuv_2023.json', 'a', encoding='utf-8') as file:
        json.dump(book_list, file, indent=4, ensure_ascii=False)
    # Друкуємо отримані дані
    # print("Ім'я автора:", author.strip())
    # print("Назва книги:", title)
    # print("Видавництво:", publisher)
    # print("Рік видачі:", year)
    # print("Кількість примірників:", copies)
    # print("ISBN:", isbn)
    # print("Перекладач(і):", ", ".join(translators))

def main():
    get_source_html(url='http://www.irbis-nbuv.gov.ua/cgi-bin/irbis_nbuv/cgiirbis_64.exe?C21COM=F&I21DBN=EC&P21DBN=EC&S21CNR=20&Z21ID=')

if __name__ == '__main__':
    main()
