# Бастапқы frozenset-тер
A = frozenset([1, 2, 3, 4])
B = frozenset([3, 4, 5, 6])

# 1) copy() – frozenset көшірмесін жасайды
C = A.copy()
print("copy():", C)

# 2) difference() немесе - 
# A-да бар, бірақ B-да жоқ элементтер
print("difference():", A.difference(B))
print("A - B:", A - B)

# 3) intersection() немесе &
# Ортақ элементтерді табады
print("intersection():", A.intersection(B))
print("A & B:", A & B)

# 4) isdisjoint()
# Ортақ элемент бар ма, соны тексереді
print("isdisjoint():", A.isdisjoint(B))

# 5) issubset() немесе <=
# C жиыны A-ның ішкі жиыны ма?
D = frozenset([1, 2])
print("issubset():", D.issubset(A))
print("D <= A:", D <= A)

# 6) issuperset() немесе >=
# A жиыны D-ны толық қамти ма?
print("issuperset():", A.issuperset(D))
print("A >= D:", A >= D)

# 7) symmetric_difference() немесе ^
# Ортақ емес элементтерді шығарады
print("symmetric_difference():", A.symmetric_difference(B))
print("A ^ B:", A ^ B)

# 8) union() немесе |
# Барлық элементтерді біріктіреді
print("union():", A.union(B))
print("A | B:", A | B)
