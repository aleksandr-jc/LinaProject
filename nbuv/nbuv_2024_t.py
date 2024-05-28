import json
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time


def get_source_html(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    book_info = []

    
    try:
        driver.get(url=url)
                # Вибір опції "Рік видання" в селекторі
        search_type_select = Select(driver.find_element(By.NAME, "S21P03"))
        search_type_select.select_by_value("G=")
        
        # Введення року видання
        year_input = driver.find_element(By.NAME, "S21STR")  
        year_input.send_keys("2024")

        # Надсилання форми
        search_button = driver.find_element(By.NAME, "C21COM1")  
        search_button.click()

        # Очікування завантаження результатів
        time.sleep(5)

        # Отримання результатів
        main_content = driver.find_element(By.CLASS_NAME, 'advanced')
        results = main_content.find_elements(By.XPATH, "//td[@width='95%']") 
        

        for result in results:
            book_info.append(result.text.strip())

        for book in book_info:
            book_info_parc(book)

            
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

def book_info_parc(book):
# форматуємо інформацію для кращого зчитання
    lines = book.split('\n')
    info = lines[2]
    info_name = lines[1].replace(',', ' ').replace('.', ' ')

# Вибираємо потрібну інформацію за допомогою регулярних виразів
    author = info_name[-1] + info_name[:-1]  # ім'я автора    
    title = re.search(r'(.*?)(?=\[Текст\])', info).group()  # назва книги
    publisher = re.search(r'([А-ЯІЇЄҐ][а-яіїєґ]+ : [^,]+)', info).group(0)  # видавництво
    year = re.search(r"(\d{4}\.)", info).group(0)  # рік видачі
    copies = re.search(r"(\d+)\sприм\.", info).group(1)  # кількість примірників
    isbn = re.search(r"ISBN\s(\d+-\d+-\d+-\d+?-\d?)", info).group(1)  # ISBN
   
  # Пошук перекладача
    translator_match = re.search(r'пер\.\s*(.*?)\s*;', info)
    translator = ""
    if translator_match:
        translator = translator_match.group(1)

    # Друкуємо отримані дані
    # print("Ім'я автора:", author.strip())
    # print("Назва книги:", title.strip())
    # print("Видавництво:", publisher.strip())
    # print("Рік видачі:", year.strip())
    # print("Кількість примірників:", copies.strip())
    # print("ISBN:", isbn.strip())
    print("Перекладач:", translator)

def main():
    get_source_html(url='http://www.irbis-nbuv.gov.ua/cgi-bin/irbis_nbuv/cgiirbis_64.exe?C21COM=F&I21DBN=EC&P21DBN=EC&S21CNR=20&Z21ID=')

if __name__ == '__main__':
    main()