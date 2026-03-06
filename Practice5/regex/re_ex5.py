import re
with open('raw.txt','r',encoding='utf-8') as fil:
    result=fil.read()
a=r'a.*b'
res=re.findall(a,result,re.I)
print(res)