import math


deg = 15
rad = deg * (math.pi / 180)
print(f"Градус: {deg} -> Радиан: {rad:.6f}")


h, b1, b2 = 5, 5, 6
t_area = ((b1 + b2) / 2) * h
print(f"Трапеция ауданы: {t_area}")


n_sides = 4
s_len = 25
p_area = (n_sides * s_len**2) / (4 * math.tan(math.pi / n_sides))
print(f"Көпбұрыш ауданы: {p_area:.1f}")


p_base, p_height = 5, 6
print(f"Параллелограмм ауданы: {float(p_base * p_height)}")