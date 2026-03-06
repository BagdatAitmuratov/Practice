import re
with open('raw.txt', 'r', encoding='utf-8') as file:
    content = file.read()

def camel_to_snake(text):
    str1 = re.sub(r'(?<!^)([A-Z])', r'_\1', text)
    return str1.lower()

words = content.split()
snake_words = [camel_to_snake(w) for w in words]

with open('snake_results.txt', 'w', encoding='utf-8') as out_file:
    out_file.write(" ".join(snake_words))