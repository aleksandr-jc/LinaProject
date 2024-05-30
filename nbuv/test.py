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

         # Вибір опції "Рік видання" в селекторі
        search_type_select = Select(driver.find_element(By.NAME, "S21P03"))
        search_type_select.select_by_value("G=")
                
                # Введення року видання
        year_input = driver.find_element(By.NAME, "S21STR")  
        year_input.send_keys("2024")

        # Надсилання форми
        search_button = driver.find_element(By.NAME, "C21COM1")  
        search_button.click()

        while True:
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

