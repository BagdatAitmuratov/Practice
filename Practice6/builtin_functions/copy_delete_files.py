import shutil
import os

with open("maatynn.txt", "w") as f:
    f.write("test content")

shutil.copy("source.txt", "destination.txt")

if os.path.exists("destination.txt"):
    os.remove("destination.txt")