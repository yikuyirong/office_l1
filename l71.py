import requests_async
import re
import os
import rarfile

def main():

    url = "3-表内除法（一）例1视频.mp4?v=12"

    d,f = os.path.splitext(url)

    print(f"{d}{f[0:4]}")






    # url = "http://ptp.jndjg.cn/空中课堂/小学/三年级/数学/2-位置与方向例2/小学数学三年级2-位置与方向例2-胡小婷.mp4"
    #
    # filename = re.findall("(?<=/)[^/]*",url)
    #
    # filename = re.split("/",url)[-1]
    #
    # print(filename)


    # print(list(filter(lambda f:f.endswith("py"),os.listdir())))


if __name__ == '__main__':
    main()
