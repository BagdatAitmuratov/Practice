with open("data.txt", "r") as file:
    content = file.read()
    print(content)

with open("data.txt", "r") as file:
    line = file.readline()
    print(line)

with open("data.txt", "r") as file:
    lines = file.readlines()
    print(lines)