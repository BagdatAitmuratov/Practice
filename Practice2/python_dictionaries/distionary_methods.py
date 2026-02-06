'''
clear()	Removes all the elements from the dictionary
copy()	Returns a copy of the dictionary
fromkeys()	Returns a dictionary with the specified keys and value
get()	Returns the value of the specified key
items()	Returns a list containing a tuple for each key value pair
keys()	Returns a list containing the dictionary's keys
pop()	Removes the element with the specified key
popitem()	Removes the last inserted key-value pair
setdefault()	Returns the value of the specified key. If the key does not exist: insert the key, with the specified value
update()	Updates the dictionary with the specified key-value pairs
values()	Returns a list of all the values in the dictionary
'''
#clear()
d = {"a": 1, "b": 2}
d.clear()
print(d) # Нәтиже: {}

#copy()
original = {"x": 10}
new_copy = original.copy()
print(new_copy) # Нәтиже: {'x': 10}

#fromkeys()
keys = ('key1', 'key2', 'key3')
d = dict.fromkeys(keys, 0)
print(d) # Нәтиже: {'key1': 0, 'key2': 0, 'key3': 0}

#get()
d = {"name": "Ali"}
print(d.get("age")) # Нәтиже: None (қате шықпайды)
print(d.get("name")) # Нәтиже: Ali

#items()
d = {"id": 1, "val": 100}
print(d.items()) # Нәтиже: dict_items([('id', 1), ('val', 100)])

#keys()
d = {"a": 1, "b": 2}
print(d.keys()) # Нәтиже: dict_keys(['a', 'b'])

#pop()
d = {"fruit": "apple", "color": "red"}
d.pop("color")
print(d) # Нәтиже: {'fruit': 'apple'}

#popitem()
d = {"a": 1, "b": 2, "c": 3}
d.popitem()
print(d) # Нәтиже: {'a': 1, 'b': 2}

#setdefault()
d = {"name": "Asan"}
d.setdefault("age", 20) 
print(d) # Нәтиже: {'name': 'Asan', 'age': 20}

#update()
d = {"a": 1}
d.update({"b": 2, "c": 3})
print(d) # Нәтиже: {'a': 1, 'b': 2, 'c': 3}

#values()
d = {"x": 5, "y": 10}
print(d.values()) # Нәтиже: dict_values([5, 10])