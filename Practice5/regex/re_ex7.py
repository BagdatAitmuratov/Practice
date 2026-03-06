import re
with open('raw.txt','r',encoding='utf-8') as file:
    res=file.read()
def snake(word):
    text=word.capitalize()
    return re.sub(r'_([a-z])',lambda x:x.group(1).upper(),text)
all_snake_words=re.findall(r'[a-z]+(?:_[a-z]+)+' ,res)
camel_words=[snake(w) for w in all_snake_words]
print(all_snake_words)
print(camel_words)