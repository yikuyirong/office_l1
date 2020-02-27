import os


def main():

    def _get_fileinfo(dir):

        files = []

        for file in os.listdir(dir):
            filename = os.path.join(dir,file)
            if os.path.isfile(filename):
                print("\r",filename,end="")
                files.append({"filename":filename,"size":os.path.getsize(filename)})
            else:
                for file in _get_fileinfo(filename):
                    files.append(file)

        return files


    dir = input("请输入你要查找的目录：")

    if dir == "":
        dir = r"d:\download\MM"

    print()

    files = sorted(_get_fileinfo(dir),key= lambda r:r["size"],reverse=True)

    for file in files[0:10]:
        print(file)


if __name__ == '__main__':
    main()
