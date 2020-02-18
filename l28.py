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

download_tasks = []

over = []

async def _download_list_page(page_index, retry=5):
    try:
        root_url = "http://av.avlang4.co/"

        list_page_url = f"{root_url}thread-htm-fid-{fid}-page-{page_index}.html"

        print(f"Retrieve list page {list_page_url}")

        resp = await requests_async.get(list_page_url)
        await resp.close()

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

            # for task in tasks:
            #     await task

            result = await asyncio.gather(*tasks)

            print(f"新增任务 {sum(result)} 个")

    except:
        if retry > 0:
            await _download_list_page(page_index, retry - 1)


async def _download_detail_page(title, imgs_name, detail_page_url, retry=5):
    try:
        resp = await requests_async.get(detail_page_url)

        await resp.close()

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

            # tasks = []

            for (index, img) in enumerate(imgs):
                page_title = f"{title} {index + 1}/{len(imgs)}"

                img_name = f"{imgs_name}-{index}.jpg"

                # await _download_img(title, img_name, img.get("src"))

                # tasks.append(_download_img(page_title, img_name, img.get("src")))

                # 生产下载任务
                # download_tasks.append(_download_img(page_title, img_name, img.get("src")))
                download_tasks.append((page_title, img_name, img.get("src")))

            return len(imgs)

            # await asyncio.gather(*tasks)
        else:
            return 0
    except:
        if retry > 0:
            return await _download_detail_page(title, imgs_name, detail_page_url, retry - 1)


async def _download_img(title, img_name, img_url, retry=10):
    try:
        # 添加UA
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}
        resp = await requests_async.get(img_url, timeout=(5, 10), headers=headers)
        # await resp.close()

        if resp.status_code == 200:
            with open(os.path.join(img_dir, img_name), "wb") as f:
                f.write(resp.content)
                print(title, f"下载文件成功:{retry}", img_name, img_url)

    except:

        if retry > 0:
            await asyncio.sleep(0.1)
            await _download_img(title, img_name, img_url, retry - 1)
        else:
            print(title, "\033[1;31m下载文件失败\033[0m", img_name, img_url)


async def main():

    async def producer(range):
        for i in range:
            await _download_list_page(i)

        over.append("over")

        print("生产协程结束")

    # 消费下载任务
    async def consumer(x):
        while len(download_tasks) > 0:
            (title, name, href) = download_tasks.pop(0)
            await _download_img(f"total:{len(download_tasks)} 协程{x} {title}", name, href)

        if len(over) == 0:
            await asyncio.sleep(2)
            await consumer(x)
        else:
            print(f"消费协程{x}结束")

    await asyncio.gather(producer(range(1, 51)), asyncio.gather(*[consumer(x) for x in range(0, 101)]))

    # for index in range(24, 101):
    #     await _download_list_page(index)
    #     await asyncio.sleep(1)

    # pages = list(range(1, 100))
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
        if not loop.is_closed():
            loop.close()

        print("\033[1;31m发生错误\033[0m", str(e))
