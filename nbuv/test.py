import re

# Вхідні дані
book = "ВА868872\nМакДоналд, Меґан Василівна.\nДжуді Муді стає знаменитою [Текст] : [повість : для мол. шк. віку] / Меґан МакДоналд ; з англ. пер. Наталія Ясіновська ; іл. Пітера Рейнолдса. - Львів : Видавництво Старого Лева, 2024. - 117, [1] с. : іл. - (Джуді Муді ; кн. 2). - 4000 прим. - ISBN 978-617-679-200-0 (укр.). - ISBN 978-1-4063-3583-5 (англ.)\nРубрикатор НБУВ:\n Ш86(7СПО)6-44 \nУДК:\n 821.111(73)'06-31-93 \nТематичні рубрики:\n Видання творів художньої літератури для дітей та юнацтва \n\nГеографічні рубрики:\n Сполучені Штати Америки (США) \n\nДод. точки доступу:\nЯсіновська, Наталія (пер.); Рейнолдс, Пітер (іл.)\n\nВидання зберігається у :\nОсновний фонд"

def book_info_parc(book):
# форматуємо інформацію для кращого зчитання
    lines = book.split('\n')
    info = str(lines[2])
    info_name = lines[1].replace(',', ' ').replace('.', ' ')

# Вибираємо потрібну інформацію за допомогою регулярних виразів
    author = info_name[-1] + info_name[:-1]  # ім'я автора    
    title = re.search(r'(.*?)(?=\[Текст\])', info).group()  # назва книги
    publisher = re.search(r'([А-ЯІЇЄҐ][а-яіїєґ]+ : [^,]+)', info).group(0)  # видавництво
    year = re.search(r"(\d{4}\.)", info).group(0)  # рік видачі
    copies = re.search(r"(\d+)\sприм\.", info).group(1)  # кількість примірників
    isbn = re.search(r"ISBN\s(\d+-\d+-\d+-\d+?-\d?)", info).group(1)  # ISBN
   
  # Пошук перекладача
    translator_match = re.search(r'пер\.\s*(.*?)\s*;', info)
    translator = ""
    if translator_match:
        translator = translator_match.group(1)


    # Друкуємо отримані дані
    print("Ім'я автора:", author.strip())
    print("Назва книги:", title.strip())
    print("Видавництво:", publisher.strip())
    print("Рік видачі:", year.strip())
    print("Кількість примірників:", copies.strip())
    print("ISBN:", isbn.strip())
    print("Перекладач:", translator)


def main():
    book_info_parc(book)

if __name__ == '__main__':
    main()