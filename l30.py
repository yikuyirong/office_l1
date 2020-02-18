#!usr/env/bin
# -*- coding:utf-8 -*-

"Get http://av.avlang4.co/thread-htm-fid-4.html"

import requests_async
import os
import re
from bs4 import BeautifulSoup
import asyncio

fid = 5

img_srcs = []

img_dir = f"avlang-fid-{fid}-images"


async def _download_list_page(page_index):
    root_url = "http://av.avlang4.co/"

    list_page_url = f"{root_url}thread-htm-fid-{fid}-page-{page_index}.html"

    resp = await requests_async.get(list_page_url)

    if resp.status_code == 200:
        resp.encoding = "GBK"
        soup = BeautifulSoup(resp.text, "html.parser")

        # <a href="read-htm-tid-1913675.html" id="a_ajax_1913675" class="subject">[MP4/ 524M]&nbsp;&nbsp;国庆福利91sex哥酒店约炮身材超棒的性感情趣高跟海归妹子.</a>
        def _filter(a):
            if a.has_attr("href"):
                return (not (a.find("font") or a.find("b"))) and \
                       re.search("read-htm-tid-\d+(-fpage-\d+)?.html",
                                 a.get("href")) \
                       and re.search(
                    "[a-zA-Z\u4e00-\u9fa5\s]+", a.text)
            else:
                return False

        a_s = list(filter(_filter, soup.find_all("a")))

        tasks = list()

        for (index, a) in enumerate(a_s):
            title = f"{page_index} {index + 1}/{len(a_s)}"
            href = f"{root_url}{a.get('href')}"
            imgs_name = "".join(re.findall(r'[^*"/:?\\|<>]', a.text, re.S))

            tasks.append(_download_detail_page(title, imgs_name, href))

        await asyncio.gather(*tasks)


async def _download_detail_page(title, imgs_name, detail_page_url):
    resp = await requests_async.get(detail_page_url)

    if resp.status_code == 200:
        resp.encoding = "GBK"
        soup = BeautifulSoup(resp.text, "html.parser")

        def _filter(img):

            src = img.get("src")

            if src not in img_srcs:
                img_srcs.append(src)
                return img.has_attr("src") and re.match("http.*jpg", img.get("src"))
            else:
                return False

        imgs = list(filter(_filter, soup.find_all("img")))

        tasks = []

        for (index, img) in enumerate(imgs):
            page_title = f"{title} {index + 1}/{len(imgs)}"

            img_name = f"{imgs_name}-{index}.jpg"

            # await _download_img(title, img_name, img.get("src"))

            tasks.append(_download_img(page_title, img_name, img.get("src")))

        await asyncio.gather(*tasks)


async def _download_img(title, img_name, img_url):
    try:
        resp = await requests_async.get(img_url,timeout=(2,3))

        if resp.status_code == 200:
            with open(os.path.join(img_dir, img_name), "wb") as f:
                f.write(resp.content)
                print(title, "下载文件成功", img_name, img_url)
    except BaseException as e:
        print(title, "\033[1;31m下载文件失败\033[0m", img_name, img_url, str(e))


async def main():

    for index in range(1,101):
        await _download_list_page(index)

    # pages = list(range(1,100))
    #
    # i = 0
    #
    # while i < len(pages):
    #     await asyncio.gather(*[_download_list_page(index) for index in pages[i: min(len(pages), i + 2)]])
    #     i = i + 2


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    try:
        if not os.path.isdir(img_dir):
            os.mkdir(img_dir)

        loop.run_until_complete(main())
    except BaseException as e:
        print("\033[1;31m发生错误\033[0m", str(e))
        loop.close()
