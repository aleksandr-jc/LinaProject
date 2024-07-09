from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def get_source_html(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    driver.maximize_window()
    info_list = []
    try:
        driver.get(url=url)
        time.sleep(3)
        
        try: 
            info_button = driver.find_element(By.XPATH, '//*[@id="product"]/div[1]/div/div/div/section/div[7]/button') 
        except:
            info_button = driver.find_element(By.XPATH, '//*[@id="product"]/div[1]/div/div/div/section/div[6]/button')

        driver.execute_script("arguments[0].scrollIntoView(true);", info_button)
        info_button.click()
        time.sleep(2)

        book_name = driver.find_element(By.XPATH, '//*[@id="product"]/div[1]/div/div/div/section/div[1]/div[2]/h1').text
                                                
        main_content = driver.find_element(By.CLASS_NAME, 'chars')

        results = main_content.find_elements(By.CLASS_NAME, 'char')

        for result in results:
            info_list.append(result.text.strip())

        return info_list, book_name

    except Exception as _ex:
        print(_ex)
    finally:
        time.sleep(1)
        driver.close()
        driver.quit()



def save_book_info(info_list):
    # Створюємо словник для зберігання інформації
    book_info = {}
    
    # Обробляємо кожен елемент списку
    for item in info_list[0]:
        # Розділяємо ключ і значення за символом нової лінії
        key, value = item.split('\n')
        
        try:# Перетворюємо числові значення в відповідний формат
            if key in ["Тираж", "Кількість сторінок", "Рік видання", "Вага"]:
                value = int(value)
        except:
            value = value
        
        # Додаємо пару ключ-значення в словник
        book_info['Назва книжки'] = info_list[1]
        book_info[key] = value
        
    
    # Зберігаємо словник у файл у форматі JSON
    with open('book_info.json', 'a', encoding='utf-8') as json_file:
        json.dump(book_info, json_file, ensure_ascii=False, indent=4)
    
    return book_info

start_time = time.time()
with open('data/yakaboo/main/book_links61_101.txt') as file:
    src = file.readlines()
# 351
# 1015
# 1904
for link in src[1904:]:
    print(f'Page: {link}')
    link = link.strip()
    info = get_source_html(link)
    save_book_info(info)

# виводимо час роботи скрипту
end_time = time.time() - start_time
print(end_time)
    