#!usr/env/bin
# -*- coding:utf-8 -*-

"Get http://av.avlang4.co/thread-htm-fid-4.html"

import requests
import requests_async
import os
import re
from bs4 import BeautifulSoup
import asyncio
from PIL import Image


class DownloadImage(object):
    _fid = 5

    __img_urls = []

    __download_tasks = []

    __is_over = False

    _root_url = None

    def __init__(self, root_url):
        self._root_url = root_url

    def _get_img_dir(self):
        raise Exception("请在子类中重写_get_img_dir(self)方法")

    def _get_list_page_url(self, page_index):
        raise Exception("请在子类中重写_get_list_page_url(self,page_index)方法")

    def _get_img_uri(self, img):
        return img.get("src")

    def _check_a_is_valid(self, a):
        return a.has_attr("href") and \
               (not (a.find("font") or a.find("b"))) and \
               re.search("topic-\d+-1-1.html", a.get("href")) and \
               re.search("[a-zA-Z\u4e00-\u9fa5]+", a.text)

    def _check_img_is_valid(self, uri):
        return re.search("http.*jpg", uri)

    async def _download_list_page(self, page_index, retry=5):

        list_page_url = self._get_list_page_url(page_index)

        try:

            print(f"刷新列表页 {list_page_url}")

            resp = await requests_async.get(list_page_url)
            # await resp.close()

            if resp.status_code == 200:

                resp.encoding = "GBK"
                soup = BeautifulSoup(resp.text, "html.parser")

                a_s = list(filter(self._check_a_is_valid, soup.find_all("a")))

                tasks = list()

                for (index, a) in enumerate(a_s):
                    title = f"第{page_index}页 第{index + 1}条/共{len(a_s)}条"
                    href = f"{self._root_url}{a.get('href')}"
                    imgs_name = "".join(re.findall(r'[^*"/:?\\|<>]', a.text, re.S))

                    tasks.append(self._get_download_tasks(title, imgs_name, href))

                # for task in tasks:
                #     await task

                result = await asyncio.gather(*tasks)

                print(f"新增任务 {sum(result)} 个")

            else:
                raise Exception(resp.status_code, resp.raise_for_status())

        except Exception as e:
            if retry > 0:
                await self._download_list_page(page_index, retry - 1)
            else:
                print("刷新列表页失败", list_page_url, str(e))

    async def _get_download_tasks(self, title, imgs_name, detail_page_url, retry=5):
        try:
            resp = await requests_async.get(detail_page_url)

            # await resp.close()

            if resp.status_code == 200:
                resp.encoding = "GBK"

                soup = BeautifulSoup(resp.text, "html.parser")

                img_urls = []

                for img_url in soup.find_all("img"):

                    img_url = self._get_img_uri(img_url)

                    if img_url and self._check_img_is_valid(img_url) and img_url not in self.__img_urls:

                        self.__img_urls.append(img_url)

                        if not img_url.startswith("http"):
                            img_url = f"{self._root_url}{img_url}"

                        img_urls.append(img_url)

                # tasks = []

                for (index, img_url) in enumerate(img_urls):
                    page_title = f"{title} {index + 1}/{len(img_urls)}"

                    ext = re.search(r"(\.jpg|\.png){1}$", img_url).group()

                    img_name = f"{imgs_name}-{index}{ext}"

                    # await _download_img(title, img_name, img_url.get("src"))

                    # tasks.append(_download_img(page_title, img_name, img_url.get("src")))

                    # 生产下载任务
                    # download_tasks.append(_download_img(page_title, img_name, img_url.get("src")))

                    self.__download_tasks.append((page_title, img_name, img_url))

                # print(imgs_name,len(img_urls))

                return len(img_urls)

                # await asyncio.gather(*tasks)
            else:
                raise Exception(f"获取下载任务失败 {title} {imgs_name} {detail_page_url}")
        except:
            if retry > 0:
                return await self._get_download_tasks(title, imgs_name, detail_page_url, retry - 1)
            else:
                return 0

    async def _download_img(self, title, img_name, img_url, retry=10):
        try:

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}

            resp = await requests_async.get(img_url, timeout=(5, 10), headers=headers)
            # await resp.close()

            if resp.status_code == 200:
                with open(os.path.join(self._get_img_dir(), img_name), "wb") as f:
                    f.write(resp.content)
                    print(title, f"下载文件成功:{retry}", img_name, img_url)
            else:
                raise Exception(f"返回错误代码{resp.status_code} 错误原因{resp.raise_for_status()}")

        except BaseException as e:
            try:
                if retry > 0:
                    await asyncio.sleep(0.1)
                    await self._download_img(title, img_name, img_url, retry - 1)
                else:
                    print(title, "\033[1;31m下载文件失败\033[0m", img_name, img_url, str(e))
            except:
                pass

    async def dowload_images(self, fid, pages, cors):

        self._fid = fid

        if not os.path.isdir(self._get_img_dir()):
            os.mkdir(self._get_img_dir())

        async def producer(range):

            # for i in range:
            #     await self._download_list_page(i)

            await asyncio.gather(*[self._download_list_page(i) for i in range], return_exceptions=True)

            self.__is_over = True

            print("生产协程结束")

        # 消费下载任务
        async def consumer(x):
            while len(self.__download_tasks) > 0:

                (title, name, href) = self.__download_tasks.pop(0)
                while True:
                    try:
                        await self._download_img(f"total:{len(self.__download_tasks)} 协程{x} {title}", name, href)
                    except BaseException as e:
                        print(f"\033[1;31m执行消费任务出错\033[0m，任务{x}", str(e))
                    else:
                        break

            if not self.__is_over:
                await asyncio.sleep(2)
                await consumer(x)
            else:
                print(f"消费协程{x}结束")

        await asyncio.gather(producer(pages), asyncio.gather(*[consumer(x) for x in range(0, cors)]))

        # 删除有问题过过小的图片

        def removeImage(title, src):
            try:

                image = Image.open(src)

                if image.width < 640 or image.height < 480:
                    print(title, src, image.width, image.height)
                    image.close()
                    os.remove(src)
                else:
                    image.close()
            except:
                print(title, f"\033[1;31m{src}\033[0m")
                os.remove(src)

        dirs = os.listdir(self._get_img_dir())

        for index, file in enumerate(dirs):
            removeImage(f"{index + 1}/{len(dirs)} {file}", os.path.join(self._get_img_dir(), file))
