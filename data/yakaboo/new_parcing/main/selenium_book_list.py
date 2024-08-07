from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from selenium.webdriver.chrome.options import Options
import os 
import shutil

def get_source_html(url):
   

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск у headless режимі
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # driver.maximize_window()
    info_list = []
    try:
        driver.get(url=url)
        time.sleep(3)
        
        try: 
            info_button = driver.find_element(By.CSS_SELECTOR, '#product > div:nth-child(1) > div > div > div > section > div.product-chars.main__chars.product-main-section > button') 
        except:
            time.sleep(1)
            info_button = driver.find_element(By.CSS_SELECTOR, '#product > div:nth-child(1) > div > div > div > section > div.product-chars.main__chars.product-main-section > button') 
        
        driver.execute_script("arguments[0].scrollIntoView(true);", info_button)
        info_button.click()
        time.sleep(1)

        book_name = driver.find_element(By.XPATH, '//*[@id="product"]/div[1]/div/div/section[1]/div[2]/div[1]/h1').text # //*[@id="product"]/div[1]/div/div/section[1]/div[2]/div[1]/h1
                                                
        main_content = driver.find_element(By.CLASS_NAME, 'chars')

        results = main_content.find_elements(By.CLASS_NAME, 'char')

        for result in results:
            info_list.append(result.text.strip())

        return info_list, book_name

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def save_book_info(info_list):
    # Створюємо словник для зберігання інформації
    book_info = {}
    
    try:
        # Обробляємо кожен елемент списку
        for item in info_list[0]:
            try:
                # Розділяємо ключ і значення за символом нової лінії
                key, value = item.split('\n')
                
                # Перетворюємо числові значення в відповідний формат
                if key in ["Тираж", "Кількість сторінок", "Рік видання", "Вага"]:
                    value = int(value)
                
                # Додаємо пару ключ-значення в словник
                book_info[key] = value
            
            except ValueError:
                # Обробляємо випадки, коли split не працює, або int(value) не працює
                continue
    
        # Додаємо назву книжки в словник
        book_info['Назва книжки'] = info_list[1]
    
    except IndexError:
        # Обробляємо випадок, коли info_list[0] або info_list[1] не існують
        pass
        
    
    # Зберігаємо словник у файл у форматі JSON
    with open('data/yakaboo/new_parcing/data/book_info.json', 'a', encoding='utf-8') as json_file:
        json.dump(book_info, json_file, ensure_ascii=False, indent=4)
    
    return book_info




def main():
    list = os.listdir('data/yakaboo/new_parcing/data/book_publisher_links')
    print(len(list))
    count = 0
    element = '[+]'

    for x in list[:30]:
        
        print(f'\nПрацюємо з цим видавництвом:  {x} \n {element * 30}\n')
        with open(f'data/yakaboo/new_parcing/data/book_publisher_links/{x}') as file:
            src = file.readlines()

        for index, link in enumerate(src):
            print(f'Index: {index} Page: {link}')
            link = link.strip()
            info = get_source_html(link)
            save_book_info(info)

        source = f'data/yakaboo/new_parcing/data/book_publisher_links/{x}'
        destination = f'data/yakaboo/new_parcing/finish_publisher/{x}'
        shutil.move(source, destination)

        count += 1
        print(count)
    print(len(list))

def main1():
    x = 'Yakaboo_ua.txt'
    with open(f'data/yakaboo/new_parcing/data/book_publisher_links/{x}') as file:
        src = file.readlines()

    for index, link in enumerate(src[154:]):
        print(f'Index: {index} Page: {link}')
        link = link.strip()
        info = get_source_html(link)
        save_book_info(info)

    source = f'data/yakaboo/new_parcing/data/book_publisher_links/{x}'
    destination = f'data/yakaboo/new_parcing/finish_publisher/{x}'
    shutil.move(source, destination)




if __name__ == "__main__":
    main()