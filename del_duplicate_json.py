import json

"""
Видаляємо дуплікати в json файлі
"""

def remove_duplicates(input_file, output_file):
    # Завантажуємо дані з файлу JSON
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Видаляємо дублікати за допомогою множини (set)
    unique_data = list({json.dumps(item, sort_keys=True) for item in data})
    unique_data = [json.loads(item) for item in unique_data]
    
    # Зберігаємо оновлені дані у файл JSON
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, ensure_ascii=False, indent=4)

# Використання функції
remove_duplicates('data/knigoland/data/processed/json/knigoland_children.json', 'data/knigoland/data/processed/json/knigoland_children.json')
