import re

text = "Менің атым Бағдат, жасым 17-те"
result = re.search(r'Бағдат', text)

if result:
    print("Табылды:", result.group()) # group() нәтижені мәтін түрінде шығарады
    print("Қай жерде (индекс):", result.span()) # Қай әріптен басталғанын көрсетеді