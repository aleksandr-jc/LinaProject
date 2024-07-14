import os 
import shutil

list = os.listdir('data/yakaboo/new_parcing/data/book_publisher_links')
count = 0
for x in list[:1]:
    count += 1
    print(x)
    source = f'data/yakaboo/new_parcing/data/book_publisher_links/{x}'
    destination = f'data/yakaboo/new_parcing/test/{x}'
    shutil.move(source, destination)
    

print(count)