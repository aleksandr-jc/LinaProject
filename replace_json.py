"""
Замінюємо '][' , ',' і переписуємо json файл
"""


def replace_in_json_file(input_file):
    # Відкриття файлу JSON для заміни
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Заміна рядків
    new_content = content.replace('][' , ',')

    # Збереження оновленого вмісту у тому ж файлі
    with open(input_file, 'w', encoding='utf-8') as file:
        file.write(new_content)

# Використання функції
replace_in_json_file('data/bookclub/fiction_books/main/book_data.json')