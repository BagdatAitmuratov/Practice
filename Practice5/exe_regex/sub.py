#sup- кез келген символды басқа символға ауыстырады
import re
text = "2024-05-10"
new_text = re.sub(r'-', '.', text)
print(new_text) 