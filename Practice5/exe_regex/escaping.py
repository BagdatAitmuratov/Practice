  # \. - нақты нүктені ғана табады
import re
text1= "Бағасы 0.99$"
res = re.findall(r'\d\.\d+', text1)
print(res)

text2 = "PP2 is so good"
res = re.findall(*(r'\w\w\d', text2))
print(res) 
