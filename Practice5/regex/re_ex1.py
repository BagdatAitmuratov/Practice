import re
with open('raw.txt','r',encoding="utf-8") as file:
    result=file.read()
g=r'ab*'
rs=re.findall(g,result,re.I)
print(len(rs))
print(rs)