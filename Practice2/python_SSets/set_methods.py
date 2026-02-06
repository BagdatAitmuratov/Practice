# Бастапқы set-тер
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print("A:", A)
print("B:", B)
print("-" * 40)

# 1) add() – set-ке бір элемент қосады
A.add(10)
print("add(10):", A)

# 2) clear() – барлық элементтерді өшіреді
C = {7, 8, 9}
C.clear()
print("clear():", C)

# 3) copy() – set көшірмесін жасайды
D = A.copy()
print("copy():", D)

# 4) difference() немесе -
# A-да бар, B-да жоқ элементтер
print("difference():", A.difference(B))
print("A - B:", A - B)

# 5) difference_update() немесе -=
# A-дан B-мен ортақ элементтерді өшіреді
E = A.copy()
E.difference_update(B)
print("difference_update():", E)

# 6) discard() – элементті өшіреді (қате шығармайды)
A.discard(2)
print("discard(2):", A)

# 7) intersection() немесе &
# Ортақ элементтер
print("intersection():", A.intersection(B))
print("A & B:", A & B)

# 8) intersection_update() немесе &=
# A-да тек ортақ элементтерді қалдырады
F = A.copy()
F.intersection_update(B)
print("intersection_update():", F)

# 9) isdisjoint()
# Ортақ элемент бар ма?
print("isdisjoint():", A.isdisjoint(B))

# 10) issubset() немесе <= , <
G = {3, 4}
print("issubset (<=):", G <= B)
print("proper subset (<):", G < B)

# 11) issuperset() немесе >= , >
print("issuperset (>=):", B >= G)
print("proper superset (>):", B > G)

# 12) pop() – кездейсоқ элементті өшіреді
H = {1, 2, 3}
removed = H.pop()
print("pop():", removed, "қалғаны:", H)

# 13) remove() – көрсетілген элементті өшіреді (жоқ болса қате)
A.remove(3)
print("remove(3):", A)

# 14) symmetric_difference() немесе ^
# Ортақ емес элементтер
print("symmetric_difference():", A.symmetric_difference(B))
print("A ^ B:", A ^ B)

# 15) symmetric_difference_update() немесе ^=
I = A.copy()
I.symmetric_difference_update(B)
print("symmetric_difference_update():", I)

# 16) union() немесе |
# Барлық элементтерді біріктіреді
print("union():", A.union(B))
print("A | B:", A | B)

# 17) update() немесе |=
# A-ны B элементтерімен толықтырады
J = A.copy()
J.update(B)
print("update():", J)
