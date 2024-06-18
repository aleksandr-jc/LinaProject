base_url = 'https://sens.in.ua/kataloh/filter/page='
listmode = '/'
start_value = 2
max_value = 402

for attempt in range(max_value):
    try:    
        url = f"{base_url}{start_value}{listmode}"
        start_value += 1 
        data = get_data(url)
    except Exception:
        print('END!')
        break