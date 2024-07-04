import json
import re

def clean_data(input_file, output_file):
    # Завантажуємо дані з файлу JSON
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Обробляємо кожен об'єкт у даних
    for item in data:
        # Видаляємо слово "Книга" (незалежно від регістру) та символи "\" з "Назва книги"
        if "Назва книги" in item and item["Назва книги"] is not None:
            original_title = item["Назва книги"]
            # Використовуємо регулярний вираз для видалення слова "Книга" з можливими наступними символами
            cleaned_title = re.sub(r'^[Кк]нига[-\s]*', '', original_title).strip()
            item["Назва книги"] = cleaned_title
            print(f"Original title: '{original_title}', Cleaned title: '{cleaned_title}'")  # Debug information
        
        # Видаляємо символи "\" з "Назва видавця"
        if "Назва видавця" in item and item["Назва видавця"] is not None:
            original_publisher = item["Назва видавця"]
            cleaned_publisher = original_publisher.replace("\"", "").strip()
            item["Назва видавця"] = cleaned_publisher
            print(f"Original publisher: '{original_publisher}', Cleaned publisher: '{cleaned_publisher}'")  # Debug information
    
    # Зберігаємо оновлені дані у файл JSON
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Використання функції
clean_data('data/knigoland/data/processed/json/knigoland_schoolchildren.json', 'data/knigoland/data/processed/json/knigoland_schoolchildren1пш.json')