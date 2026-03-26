with open("output.txt", "w") as file:
    file.write("Hello Python\n")

with open("output.txt", "a") as file:
    file.write("Appending new line\n")

try:
    with open("new_file.txt", "x") as file:
        file.write("Exclusive creation")
except FileExistsError:
    pass