import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

rootUrl = "http://av.avlang4.co/"

imgs_src = []

downloadDir = "Images"


def _get_detail_page(index):
    listUrl = "%sthread-htm-fid-9-page-%d.html" % (rootUrl, index)

    resp = requests.get(listUrl)

    if resp.status_code == 200:

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

        # http://av.avlang4.co/read-htm-tid-1553613.html

        def _filterurl(a):
            if a.has_attr("href"):
                href = a.get("href")
                text = a.text

                return re.match("^read-htm-tid-\d+(-fpage-\d+)?.html$", href) and re.match("[a-zA-Z\u4E00-\u9FA5\s]+",
                                                                                           text)
            else:
                return False

        print("刷新成功", listUrl)

        L = list(filter(_filterurl, soup.find_all("a")))

        for (i, a) in enumerate(L):
            # print(a.text, a.get("href"))
            _get_image_url(f"{index} {i + 1}/{len(L)}", a.text, a.get("href"))


    else:
        print("刷新失败", listUrl)


def _get_image_url(index, name, detailUrl):
    detailUrl = "%s%s" % (rootUrl, detailUrl)

    resp = requests.get(detailUrl)

    if resp.status_code == 200:

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

        def _filterimg(img):
            if img.has_attr("src"):
                src = img.get("src")
                return src.startswith("http") and src.endswith("jpg") and src not in imgs_src

        L = list(filter(_filterimg, soup.find_all("img")))

        for (i, img) in enumerate(L):
            title = "%s-%d.jpg" % (name, i + 1)

            src = img.get("src")

            _download_img(f"{index} {i + 1}/{len(L)}", title, src)

            imgs_src.append(src)




    else:
        print("获取图像链接失败")


def _download_img(index, name, src):
    try:
        resp = requests.get(src, timeout=(2, 3))

        with open(os.path.join(downloadDir, name), "wb") as f:
            f.write(resp.content)

        print(index, "下载成功", name, src, datetime.now())

    except:
        print(index, "下载失败", name, src, datetime.now())


if __name__ == "__main__":

    import os

    if not os.path.isdir(downloadDir):
        os.mkdir(downloadDir)

    for i in range(12, 20):
        _get_detail_page(i)
