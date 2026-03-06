import re

with open('raw.txt', 'r', encoding='utf-8') as file:
    content = file.read()
pattern = r'([A-Z])'
result = re.sub(r'(?<!^)' + pattern, r' \1', content)

with open('output2.txt', 'w', encoding='utf-8') as out_file:
    out_file.write(result)
