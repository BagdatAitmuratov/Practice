import re
with open('raw.txt','r',encoding='utf-8') as file:
    result=file.read()
a=r'[a-z]+_[a-z]+'
res=re.findall(a,result)
print(res)