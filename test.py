import re

def remove_author(text):
    return re.sub(r'\.\s*[^.]+$', '.', text)

input_text = "Як ми назвемо цю війну?."
output_text = remove_author(input_text)
print(output_text)