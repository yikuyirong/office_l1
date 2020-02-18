
import os

import shutil

path = "D:\download\MM\8349635\蕾丝兔宝宝2\TMP"

def moveSubDirFiles(path):

    hasModify = False

    for subPath in os.listdir(path):

        oldpath = os.path.join(path,subPath)

        if os.path.isdir(oldpath):
            if len(os.listdir(oldpath)) == 0:
                os.rmdir(oldpath)
                print("delete %s" % oldpath)
                hasModify = hasModify or True
            else:
                hasModify = hasModify or moveSubDirFiles(oldpath)
        else:

            if subPath.lower().endswith("jpg"):
                ss = os.path.split(path)
                newPath = os.path.join(ss[0], "%s-%s" % (ss[1], subPath))
                shutil.move(oldpath, newPath)
                print("move %s to %s" % (oldpath, newPath))
            else:
                os.remove(oldpath)

            hasModify = hasModify or True

        continue

    return hasModify


while moveSubDirFiles(path):
    pass




