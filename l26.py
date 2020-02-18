
from PIL import Image

import os

image_dir = "avlang-fid-43-images"

def deletefile(src):
    try:
        os.remove(src)
    except BaseException as e:
        print(f"\033[1;31m删除失败\033[0m",str(e))


L = os.listdir(image_dir)

for (index,name) in enumerate(L):

    src = os.path.join(image_dir,name)

    try:

        image = Image.open(src)

        if image.width < 640 or image.height < 480:
            print(f"{index}/{len(L)}",name,image.width,image.height)
            image.close()
            deletefile(src)
        else:
            image.close()
    except:
        print(f"{index}/{len(L)}",f"\033[1;31m{name}\033[0m")

        deletefile(src)



