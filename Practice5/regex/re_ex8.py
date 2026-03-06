import re
with open('raw.txt','r',encoding='utf-8') as file:
    res=file.read()
a=r'(?=[A-Z])'
b=re.split(a,res)
print(b)
with open('ouput.txt1','w',encoding='utf-8') as file_out:
    for i in b:
        file_out.write(i+'\n')
