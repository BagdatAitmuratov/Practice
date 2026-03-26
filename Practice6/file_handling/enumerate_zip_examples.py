names = ["Aman", "Asel", "Ivan"]
scores = [85, 92, 78]

for index, name in enumerate(names, start=1):
    print(index, name)

combined = list(zip(names, scores))
print(combined)