import requests_async
from bs4 import BeautifulSoup
import re
from datetime import datetime
import asyncio

rootUrl = "http://av.avlang4.co/"

imgs_src = []

downloadDir = "asiaImages"


async def _get_detail_page_async(index):
    listUrl = "%sthread-htm-fid-5-page-%d.html" % (rootUrl, index)

    resp = await requests_async.get(listUrl)

    if resp.status_code == 200:

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

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

        print(L)

        # tasks = [_get_image_url_async(f"{index} {i + 1}/{len(L)}", "".join(re.findall(r'[^*"/:?\\|<>]', a.text, re.S)), a.get("href")) for (i, a) in enumerate(L)]
        #
        #     # await _get_image_url_async(f"{index} {i + 1}/{len(L)}", a.text, a.get("href"))
        #
        # await asyncio.gather(*tasks)


    else:
        print("刷新失败", listUrl)


async def _get_image_url_async(index, name, detailUrl):

    detailUrl = "%s%s" % (rootUrl, detailUrl)

    resp = await requests_async.get(detailUrl)

    if resp.status_code == 200:

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

        def _filterimg(img):
            if img.has_attr("src"):
                src = img.get("src")
                return src.startswith("http") and src.endswith("jpg") and src not in imgs_src

        L = list(filter(_filterimg, soup.find_all("img")))

        tasks = []

        for (i, img) in enumerate(L):

            title = "%s-%d.jpg" % (name, i + 1)

            src = img.get("src")

            imgs_src.append(src)

            tasks.append(_download_img_async(f"{index} {i + 1}/{len(L)}", title, src))

        await asyncio.gather(*tasks)
        # await asyncio.wait(tasks)

    else:
        print("获取图像链接失败")


async def _download_img_async(index, name, src):
    try:
        # resp = await requests_async.get(src, timeout=(2, 3))
        resp = await requests_async.get(src)

        with open(os.path.join(downloadDir, name), "wb") as f:
            f.write(resp.content)

        print(index, "下载成功", name, src, datetime.now())

    except BaseException as e :
        print(index, "\033[1;31m下载失败\033[0m", name, src, datetime.now(),str(e))


async def main():

    # tasks = [_get_detail_page_async(i) for i in range(1, 11)]
    #
    # await asyncio.gather(*tasks)

    for i in range(6, 7):
        await _get_detail_page_async(i)


if __name__ == "__main__":

    import os

    if not os.path.isdir(downloadDir):
        os.mkdir(downloadDir)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except BaseException as e :
        loop.close()
        print(str(e))

