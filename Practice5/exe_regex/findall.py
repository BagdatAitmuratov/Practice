import re
text="Мен КБТУ да оқимын"
res=re.findall(r'КБТУ',text)
print(f"Бағдат {res}-да оқиды")