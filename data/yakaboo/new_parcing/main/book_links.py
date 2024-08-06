import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

"""
Збирає ссилки книг з кожного видавництва
Список видавництв з ссилками на них отримуємо в файлі publisher_links.txt
"""
def scroll_page(url):
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Запуск у headless режимі
    # chrome_options.add_argument("--disable-gpu")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager()))
        driver.maximize_window()
        driver.get(url)

        project_urls = []
        print(url)
        book_publisher_name = url.split('/')[-1]
        while True:
            try:
                scrol_button = driver.find_element(By.CSS_SELECTOR, '#viewport > div.entity-wrapper > div.etm-entity > div.category__content.etm-entity-content > div.category__main > div.category__more > div > button')
                driver.execute_script("arguments[0].scrollIntoView(true);", scrol_button)
                time.sleep(1)
                scrol_button.click()
                time.sleep(1)
            except:
                try:
                    scrol_button = driver.find_element(By.XPATH, '//*[@id="viewport"]/div[9]/div[2]/div[2]/div[2]/div[3]/div/button')
                    driver.execute_script("arguments[0].scrollIntoView(true);", scrol_button)
                    time.sleep(1)
                    scrol_button.click()
                    time.sleep(1)
                except:
                    break
        print('End of scroling!')
        results = driver.find_elements(By.CLASS_NAME, 'category-card.category-layout')

        for result in results:
            try:
                # Знайти перший тег <a> всередині кожного result
                link = result.find_element(By.TAG_NAME, 'a')
                # Отримати атрибут href
                href = link.get_attribute('href')
                project_urls.append(href)
                print(href)
            except Exception as e:
                print(f"Link not found in result: {e}")

        with open(f'data/yakaboo/new_parcing/data/book_publisher_links/{book_publisher_name}.txt', 'a') as file:
            for link in project_urls:
                file.write(f"{link}\n")
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


# https://www.yakaboo.ua/ua/book_publisher/view/Navchal_na_kniga_Bogdan

scroll_page('https://www.yakaboo.ua/ua/book_publisher/view/Yakaboo_Publishing')
print('Finish!')