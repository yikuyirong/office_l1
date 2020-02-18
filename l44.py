import os
import asyncio
import requests_async
from bs4 import BeautifulSoup

from PIL import Image

import PyPDF2

download_dir = "Chinese"


async def _fetch_img_url():
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)

    url = "https://mp.weixin.qq.com/s?srcid=&scene=23&sharer_sharetime=1580188309519&mid=2247491953&sharer_shareid=dc66b101b997fea5e9aad2afce1806b6&sn=d4ad82cd8e24df3ba87ae22b58c484c3&idx=3&__biz=MzI0MjQ3ODkyOQ%3D%3D&chksm=e9791b4fde0e92592ae4faa8139a98b6ac4f2521e18e618ed6b504d6f5a635ecd138eee6d129&mpshare=1#rd"

    resp = await requests_async.get(url)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")

        tasks = [(index, img) for index, img in
                 enumerate(
                     map(lambda i: i.get("data-src"), filter(lambda i: i.has_attr("data-src"), soup.find_all("img"))))]

        await asyncio.gather(*[_download_img(index, img) for (index, img) in tasks])

        # 合并pdf

        print("正在合并Pdf...")

        merger = PyPDF2.PdfFileMerger()

        # for file in sorted(os.listdir(download_dir)):
        #     with open(os.path.join(download_dir,file),"rb") as f:
        #         print(f.name)
        #         merger.append(f)
        #
        # with open(os.path.join(download_dir,"Result.pdf"),"wb") as f:
        #     merger.write(f)

        output = PyPDF2.PdfFileWriter()

        for file in sorted(os.listdir(download_dir)):
            input = PyPDF2.PdfFileReader(open(os.path.join(download_dir, file), "rb"))

            output.addPage(input.getPage(0))

        with open(os.path.join(download_dir, "Result.pdf"), "wb") as f:
            output.write(f)

        print("合并成功。")


async def _download_img(index, url):
    print("开始下载", index, url)

    resp = await requests_async.get(url)

    if resp.status_code == 200:
        name = "%03d" % index
        f = open(os.path.join(download_dir, f"{name}.webp"), "wb")
        f.write(resp.content)
        print("下载成功", index, f.name, url)
        # Image.open(f.name).save(os.path.join(download_dir, f"{name}.jpg"), "JPEG")
        Image.open(f.name).save(os.path.join(download_dir, f"{name}.pdf"), "PDF")
        print("转换成功", index, url)
        f.close()
        os.remove(f.name)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.run_until_complete(_fetch_img_url())
