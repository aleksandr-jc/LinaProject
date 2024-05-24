import json
from collections.abc import Hashable

def make_hashable(item):
    """Перетворює об'єкти на хешовані, щоб можна було використовувати set для видалення дублікатів."""
    if isinstance(item, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in item.items()))
    if isinstance(item, list):
        return tuple(make_hashable(e) for e in item)
    if isinstance(item, set):
        return tuple(sorted(make_hashable(e) for e in item))
    if isinstance(item, tuple):
        return tuple(make_hashable(e) for e in item)
    return item  # для хешованих типів (str, int, float тощо)

def remove_duplicates(input_file, output_file):
    # Завантажуємо дані з файлу JSON
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Використовуємо set для видалення дублікатів
    unique_data = list({make_hashable(item): item for item in data}.values())

    # Зберігаємо оновлені дані у файл JSON
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, ensure_ascii=False, indent=4)

# Використання функції
remove_duplicates('data/bookclub/book_data.json', 'data/no_duplicate_bookclub_data.json')
