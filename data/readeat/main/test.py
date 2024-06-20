from bs4 import BeautifulSoup

src = """
<ol class="breadcrumb overflow-auto flex-nowrap">
        <li class="breadcrumb-item d-flex text-nowrap"><a href="https://readeat.com">Головна</a></li>
                    <li class="breadcrumb-item d-flex text-nowrap ">
                                    <a href="https://readeat.com/catalog/non-fiksn-knigi">Нон-фікшн література</a>
                      
            </li>
                    <li class="breadcrumb-item d-flex text-nowrap ">
                                    <a href="https://readeat.com/catalog/psihologiya">Психологія та стосунки</a>
                      
            </li>
                    <li class="breadcrumb-item d-flex text-nowrap active">
                                    Есенціалізм. Мистецтво визначати пріоритети
                      
            </li>
            </ol>
<li class="breadcrumb-item d-flex text-nowrap"><a href="https://readeat.com">Головна</a></li>
<a href="https://readeat.com">Головна</a>
<li class="breadcrumb-item d-flex text-nowrap"><a href="https://readeat.com">Головна</a></li>
<li class="breadcrumb-item d-flex text-nowrap ">
                                    <a href="https://readeat.com/catalog/non-fiksn-knigi">Нон-фікшн література</a>
                      
            </li>
<<pseudo>></<pseudo>>
<a href="https://readeat.com/catalog/non-fiksn-knigi">Нон-фікшн література</a>
<li class="breadcrumb-item d-flex text-nowrap ">
                                    <a href="https://readeat.com/catalog/non-fiksn-knigi">Нон-фікшн література</a>
                      
            </li>
<li class="breadcrumb-item d-flex text-nowrap ">
                                    <a href="https://readeat.com/catalog/psihologiya">Психологія та стосунки</a>
                      
            </li>
<<pseudo>></<pseudo>>
<a href="https://readeat.com/catalog/psihologiya">Психологія та стосунки</a>
<li class="breadcrumb-item d-flex text-nowrap ">
                                    <a href="https://readeat.com/catalog/psihologiya">Психологія та стосунки</a>
                      
            </li>
<li class="breadcrumb-item d-flex text-nowrap active">
                                    Есенціалізм. Мистецтво визначати пріоритети
                      
            </li>
<ol class="breadcrumb overflow-auto flex-nowrap">
        <li class="breadcrumb-item d-flex text-nowrap"><a href="https://readeat.com">Головна</a></li>
                    <li class="breadcrumb-item d-flex text-nowrap ">
                                    <a href="https://readeat.com/catalog/non-fiksn-knigi">Нон-фікшн література</a>
                      
            </li>
                    <li class="breadcrumb-item d-flex text-nowrap ">
                                    <a href="https://readeat.com/catalog/psihologiya">Психологія та стосунки</a>
                      
            </li>
                    <li class="breadcrumb-item d-flex text-nowrap active">
                                    Есенціалізм. Мистецтво визначати пріоритети
                      
            </li>
            </ol>"""



soup = BeautifulSoup(src, 'lxml')
src = soup.find('nav', ar)
# print(soup)
def get_genre(soup):
    try:
        first_li = soup.find('li', class_='breadcrumb-item d-flex text-nowrap')

        if first_li:
            second_li = first_li.find_next('li', class_="breadcrumb-item d-flex text-nowrap")
            if second_li:
                third_li = second_li.find_next('li', class_='breadcrumb-item d-flex text-nowrap')
                if third_li:
                    return third_li.text.strip()

    except Exception:
        return None
    
print(get_genre(soup))