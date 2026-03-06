import re
with open('raw.txt','r',encoding='utf-8') as fa:
    resule=fa.read()
e1=r'\.'
e2=r':'
rs=re.sub(e1,e2,resule)
print(rs)
