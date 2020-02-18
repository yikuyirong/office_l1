import requests_async
from bs4 import BeautifulSoup
import asyncio
import re

# rootUrl = "http://38.103.161.132/forum/"

rootUrl = "http://av.avlang4.co/"

async def get_detail_page_url(index):

    url = "%s/thread-htm-fid-9-page-%d.html" % (rootUrl, index)

    print(url)

    resp = await requests_async.get(url)

    print(resp.status_code)

    if resp.status_code == 200:
        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

        urls = set()

        for a in soup.find_all("a"):
            # if a.has_attr("href") and a.get("href").startswith("thread"):
            if a.has_attr("href") and a.get("href").startswith("read-"):
                detail_url = '%s%s' % (rootUrl, a.get("href"))

                print(detail_url)

                urls.add(detail_url)

        return urls

    else:
        print("下载失败", url)

        return set()

async def get_jpg_url(url):
    resp = await requests_async.get(url)

    if resp.status_code == 200:

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

        title = re.findall(r'[^*"/:?\\|<>]', soup.title.text.split(" ")[0], re.S)
        title = "".join(title)

        imgs = dict()

        i = 0
        for img in soup.find_all("img"):
            if img.has_attr("src"):
                src = img.get("src")
                if src.startswith("http") and src.endswith("jpg"):
                    name = "%s-%d.jpg" % (title, i)
                    imgs[name] = src
                    print("添加图像", url, src)
                    i = i + 1
        return imgs
    else:
        return dict()


async def main():

    tasks = [get_detail_page_url(x) for x in range(1,2)]

    (success,failure) = await asyncio.wait(tasks)

    urls = set()

    for t in success:
        urls = urls.union(t.result())

    print(len(urls))

    tasks = [get_jpg_url(url) for url in urls]

    (success,failure) = await asyncio.wait(tasks)

    with open("img_urls.txt","w") as f:

        for t in success:
            for (name,url) in t.result():
                f.write("%s %s\n" % (name,url))


el = asyncio.get_event_loop()

el.run_until_complete(main())


