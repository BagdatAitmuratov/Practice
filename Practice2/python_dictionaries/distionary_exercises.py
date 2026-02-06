fruits = {}
fruits["apple"] = 5
fruits["banana"] = 10
fruits["apple"] = 7  # Мәнді жаңарту

print(fruits) # {'apple': 7, 'banana': 10}
#-----------------
keys = ['name', 'age', 'city']
values = ['Ali', 20, 'Almaty']

# zip арқылы біріктіру
user_info = dict(zip(keys, values))

print(user_info) # {'name': 'Ali', 'age': 20, 'city': 'Almaty'}
#------------------
car = {"brand": "Tesla", "model": "S"}

if "year" in car:
    print("Бар")
else:
    print("Жоқ") # "Жоқ" деп шығады
#------------
student = {"name": "Asan", "age": 18, "grade": "A"}
student.pop("age")

print(student) # {'name': 'Asan', 'grade': 'A'}
#----------------
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
squares = {x: x**2 for x in range(1, 6)}

print(squares)