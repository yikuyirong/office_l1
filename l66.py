import re
import os


def main():

    filename_2 = r"d:\his_desktop\Desktop\重庆四川2.txt"

    files_2 = []

    filename_1 = r"d:\his_desktop\Desktop\重庆四川.txt"

    files_1 = []

    with open(filename_2,encoding="gbk") as f:
        content = f.read()
        files_2 = re.findall("\d{4}.+\.jpg",content)

    with open(filename_1,encoding="utf-8") as f:
        content = f.read()
        files_1 = re.findall("\d{4}.+\.jpg",content)

    for file in sorted([file for file in files_2         if file not in files_1]):
        print(file)








if __name__ == '__main__':
    main()