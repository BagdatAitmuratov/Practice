import re
text = input("Kез келген 2 сөз жазыңыз: ")
res = re.sub(r'(\w+) (\w+)', r'\2 \1', text)
print(res)