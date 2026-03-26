import os

if not os.path.exists("new_folder"):
    os.mkdir("new_folder")

os.makedirs("parent/child/grandchild", exist_ok=True)

items = os.listdir(".")
print(items)

qai_fileda_turganyn_anyktaidy= os.getcwd()
print(qai_fileda_turganyn_anyktaidy)