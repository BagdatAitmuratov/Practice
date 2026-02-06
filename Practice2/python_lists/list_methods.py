#Элементтерді қосу және біріктіру---------------------------------------
# append() - соңына бір элемент қосу
numbers = [1, 2, 3]
numbers.append(4)
print(numbers) # [1, 2, 3, 4]

# extend() - тізімге тізімді қосу
extra = [5, 6]
numbers.extend(extra)
print(numbers) # [1, 2, 3, 4, 5, 6]

# insert() - белгілі бір индекске қосу (0-ден басталады)
numbers.insert(0, 0)
print(numbers) # [0, 1, 2, 3, 4, 5, 6]

#Элементтерді жою----------------------------------------
# remove() - мәні бойынша бірінші кездескен элементті жою
colors = ["red", "blue", "green", "blue"]
colors.remove("blue") 
print(colors) # ["red", "green", "blue"]

# pop() - көрсетілген индекстегі элементті алып тастайды және қайтарады
last_item = colors.pop() # индексті жазбасаңыз, ең соңғысын алады
print(colors) # ["red", "green"]

# clear() - тізімді толық тазалау
colors.clear()
print(colors) # []
#Іздеу және санау 
# count() - элементтің тізімде неше рет кездесетінін санау
items = ["A", "B", "A", "C"]
print(items.count("A")) # 2

# index() - элементтің бірінші кездескен индексін табу
print(items.index("B")) # 1
 
#Реттеу және көшіру----------------------------------
# sort() - тізімді өсу ретімен сұрыптау
vals = [5, 2, 9, 1]
vals.sort()
print(vals) # [1, 2, 5, 9]

# reverse() - тізімді кері айналдыру
vals.reverse()
print(vals) # [9, 5, 2, 1]

# copy() - тізімнің көшірмесін жасау
new_vals = vals.copy()
print(new_vals) # [9, 5, 2, 1]