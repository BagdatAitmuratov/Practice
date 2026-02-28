# 1. Квадраттар генераторы
def square_gen(N):
    for i in range(N + 1):
        yield i ** 2

# 2. Жұп сандарды үтірмен шығару
def even_gen(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)

n_val = int(input("Сан енгізіңіз (n): "))
print("Жұп сандар:", ", ".join(even_gen(n_val)))

def div_3_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

print("Квадрат:")
for s in squares(2, 5):
    print(s)

#Кері санау
def countdown(n):
    while n >= 0:
        yield n
        n -= 1