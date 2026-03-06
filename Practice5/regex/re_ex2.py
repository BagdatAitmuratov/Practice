import re
with open('raw.txt','r',encoding='utf-8') as file:
    result=file.read()
f=r'ab{2,3}'
res=re.findall(f,result,re.I)
print(res)