# -*- coding:utf-8 -*-

import requests

from bs4 import BeautifulSoup

from urllib.request import urlretrieve

import os

import time

import re

imageDir = "images"

if not os.path.isdir(imageDir):
    os.mkdir(imageDir)

rootUrl = "http://38.103.161.132/forum/"

rootUrl = "http://av.avlang4.co/"

def _downlaod_images(url):

    print("detailPage" , url)

    resp = requests.get(url)

    if resp.status_code == "200":

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

        title = re.findall(r'[^*"/:?\\|<>]', soup.title.text.split(" ")[0], re.S)

        title = "".join(title) #文件名

        i = 0

        for img in soup.find_all("img"):
            if img.has_attr("src"):
                src = img.get("src")
                if src.startswith("http") and src.endswith("jpg"):
                    name = "%s-%d.jpg" % (title, i)
                    _download_image(name,src)

def _download_image(name, url):
    try:
        print(name,url)
        time.sleep(0.5)
        urlretrieve(url, os.path.join(imageDir, name))
        print("下载成功", name)
    except:
        print("下载失败", name)


for x in range(1, 2):

    url = '%s/forum-25-%d.html' % (rootUrl, x)
    url = '%sthread-htm-fid-9-page-%d.html' % (rootUrl, x)

    prefix = "thread"
    prefix = "read-htm"

    print("listpage",url)

    time.sleep(1)

    headers = dict()

    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"

    #获取列表页内容
    resp = requests.get(url,headers=headers)

    if resp.status_code == 200:
        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

        for a in soup.find_all("a"):

            if a.has_attr("href") and a.get("href").startswith(prefix):
                url = '%s%s' % (rootUrl, a.get("href"))

                print(a.text, url)
                _downlaod_images(url)

    else:
        print("解析失败", url)



#
# if len(urls) > 0:
#
#     imgs = dict()
#
#     with open("urls.text", "w") as f:
#
#         for url in urls:
#
#             resp = requests.get(url)
#
#             if resp.status_code == 200:
#
#                 resp.encoding = "GBK"
#
#                 soup = BeautifulSoup(resp.text, "html.parser")
#
#                 title = re.findall(r'[^*"/:?\\|<>]', soup.title.text.split(" ")[0], re.S)
#                 title = "".join(title)
#
#                 i = 0
#                 for img in soup.find_all("img"):
#                     if img.has_attr("src"):
#                         src = img.get("src")
#                         if src.startswith("http") and src.endswith("jpg"):
#                             name = "%s-%d.jpg" % (title, i)
#                             imgs[name] = src
#                             print("添加图像",url, src)
#                             f.write("%s %s\n" % (name,src))
#                             i = i + 1
#
   # if len(imgs) > 0:
    #
    #     for (name, src) in imgs.items():
    #         try:
    #             urlretrieve(src, os.path.join(imageDir, name))
    #         except:
    #             print("下载失败")

# print(list(filter(lambda r: not r.startswith("_"), dir(resp))))

# if resp.status_code == 200:
#     resp.encoding = "GBK"
#     # print(resp.text)
#
#     soup = BeautifulSoup(resp.text,"html.parser")
#
#     print(dir(soup.a))
#
#     for x in soup.find_all("img") :
#         if x.has_attr("src") and x.get("src").endswith("jpg"):
#             print(soup.title.text.split(" ")[0])
#             print(x.get("src"))
#
#     # for x in filter(lambda r: r.get("href" != None and r.get("href").startswith("thread"),soup.find_all("a")) :
#     #     print(x)


# else:
#     print(resp.raise_for_status())


# print(content)
