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

        start_value = 21
        step = 20

        time.sleep(3)
         # Вибір опції "Рік видання" в селекторі
        search_type_select = Select(driver.find_element(By.NAME, "S21P03"))
        search_type_select.select_by_value("G=")
                
                # Введення року видання
        year_input = driver.find_element(By.NAME, "S21STR")  
        year_input.send_keys("2024")

        # Надсилання форми
        search_button = driver.find_element(By.NAME, "C21COM1")  
        search_button.click()

        while start_value != 81:
            try:
                # Очікування завантаження результатів
                time.sleep(5)

                # Отримання результатів
              
                main_content = driver.find_element(By.CLASS_NAME, 'advanced')
                results = main_content.find_elements(By.XPATH, "//td[@width='95%']")

                for result in results:
                    book_info.append(result.text.strip())
                    
                
                time.sleep(5)
                
                 # Формування значення для атрибуту value
                value = str(start_value)
                
                # Пошук елемента за його значенням value і клікаємо на нього
                button = driver.find_element(By.XPATH, f"//input[@type='submit' and @value='{value}']")
                button.click()
                
                # Чекати кілька секунд, щоб сторінка завантажилась (при необхідності)
                time.sleep(5)
                
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

def extract_translators(info):
    # Регулярний вираз для пошуку інформації про перекладача
    translator_pattern = re.compile(r'\[пер\.\s*(з\s*[а-яіїєґ]+\.\s*|із\s*[а-яіїєґ]+\.\s*)?(.*?)\s*\]')
    
    # Пошук всіх збігів у тексті
    translators = translator_pattern.findall(info)
        
        # Витягування мови з якої переклали
    # source_language = [translator[0].strip() for translator in translators]

        # Витягування імен перекладачів
    translator_names = [translator[1].strip() for translator in translators]
    
    
    return translator_names

def book_info_parc(book):
    # Форматуємо інформацію для кращого зчитання
    lines = book.split('\n')
    try:
        info = lines[2]
    except Exception:
        info = lines

    try:
        info_name = lines[1].replace(',', '').replace('.', ' ')
        # Вибираємо потрібну інформацію за допомогою регулярних виразів
        author = info_name[-1] + info_name[:-1].strip()  # ім'я автора           
    except Exception:
        author = ''

    try:
        title_match = re.search(r'(.*?)(?=\[Текст\])', info)
        title = title_match.group().strip() if title_match else "Невідома назва"  # назва книги
    except Exception: 
        title = book
        
    try:
        publisher_match = re.search(r'([А-ЯІЇЄҐ][а-яіїєґ]+ : [^,]+)', info)
        publisher = publisher_match.group().strip() 
    except Exception:
        publisher = "Невідоме видавництво"  # видавництво
    
    try:
        year_match = re.search(r"(\d{4})\.", info)
        year = year_match.group().replace('.', '').strip() 
    except Exception:
        year = "2024"  # рік видачі
    
    try: 
        copies_match = re.search(r"(\d+)\sприм\.", info)
        copies = copies_match.group(1).strip()
    except Exception:
        copies = "Невідома кількість примірників"  # кількість примірників
    
    try:
        isbn_match = re.search(r"ISBN\s(\d+-\d+-\d+-\d+-\d?)", info)
        isbn = isbn_match.group(1).strip() 
    except Exception:
        isbn = "Невідомий ISBN"  # ISBN

    # Пошук перекладачів
    try:
        translators = extract_translators(info)
    except Exception:
        translators = ''

    # зберігаю в json файлі
    book_list = []
    book_list.append(
        {
            "Ім'я автора": author.strip(),
            "Назва книги": title,
            "Видавництво": publisher,
            "Рік видачі": year,
            "Кількість примірників": copies,
            "ISBN": isbn,
            "Перекладач(і)": ", ".join(translators),            
        },
    )

    with open('data/nbuv/2024/main/nbuv_2024_json.json', 'a', encoding='utf-8') as file:
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
