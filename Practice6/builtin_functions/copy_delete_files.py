import shutil
import os
with open("bag.txt","w")as file:
    file.write("hello my name is BAGDAT!!I'm from Aral")
shutil.copy("bag.txt","copy_bag.txt")
# болек файлға лактр
# |
# |
# V
if os.path.exists("copy_bag.txt"):
    os.remove("copy_bag.txt")
    print("File oshirildi")
else:
    print("жайлы жок табылмады")
# сол кезде ошеди