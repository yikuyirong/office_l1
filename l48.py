
import os

def listdirex(dir):
    return list(map(lambda x:os.path.join(dir,x),os.listdir(dir)))

files = listdirex(r"d:\his_desktop")

print(files)


