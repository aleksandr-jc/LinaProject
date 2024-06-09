import json
import pandas as pd
"""
Заміна в json '][' на ',' та зміна формату json на excel, файл не змінюється
"""
year_of_search = '1991'
def fix_json_format(input_file):
    # Читаємо вміст файлу
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Видаляємо зайві символи та об'єднуємо всі масиви в один
    content = content.replace('][', ',')
    
    # Перетворюємо текст у JSON об'єкт
    data = json.loads(content)
    return data

def json_to_excel(input_file, output_file):
    # Виправляємо формат JSON
    data = fix_json_format(input_file)
    
    # Створюємо DataFrame з JSON данихg
    df = pd.DataFrame(data)
    
    # Записуємо дані у файл Excel
    df.to_excel(output_file, index=False, engine='openpyxl')

# Використання функції
json_to_excel(f'data/nbuv/{year_of_search}/data/nbuv_{year_of_search}.json', f'data/nbuv/{year_of_search}/data/nbuv_{year_of_search}.xlsx')
