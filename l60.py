import asyncio
import requests_async
from bs4 import BeautifulSoup
import os
import re
from PIL import Image, ImageDraw, ImageFont


async def fetch_data(url, *, exdata=None, contentHandler=None, soupHandler=None, retry=5, encoding="utf-8"):
    try:

        resp = await requests_async.get(f"http://www.h3c.com{url}")

        if contentHandler:
            await contentHandler(exdata, resp.content)
        else:
            resp.encoding = "utf-8"

            soup = BeautifulSoup(resp.text, "html.parser")

            if soupHandler:
                await soupHandler(soup)


    except BaseException as e:
        if retry > 0:
            if contentHandler:
                await fetch_data(url, exdata=exdata, contentHandler=contentHandler, retry=retry - 1, encoding=encoding)
            elif soupHandler:
                await fetch_data(url, exdata=exdata, soupHandler=soupHandler, retry=retry - 1, encoding=encoding)
            else:
                raise e


async def main():
    root_url = "/cn/Products___Technology/Products/Switches"

    imgs_dir = "h3c_imgs"

    async def _download_img(exdata, content):
        # print(exdata)
        (alt, src) = exdata
        filename = os.path.join(imgs_dir, f"{alt}-{re.search('[^/]+.jpg$', src).group()}")
        with open(filename, "wb") as f:
            f.write(content)
            print("下载成功...", filename)

        try:
            image = Image.open(filename)
            image_draw = ImageDraw.Draw(image)
            title_font = ImageFont.truetype(font=r"c:\windows\fonts\simsun.ttc", size=20)
            image_draw.text(xy=(2, 2), text=alt, fill="green" ,font=title_font)
            image.save(filename,"JPEG")

        except BaseException as e:
            print("写入标记失败")
        else:
            print("写入标记成功", alt)

    async def _handle_get_img(soup):

        tasks = []

        for img in [div.find("img") for div in soup.find_all("div", attrs={"class": "img ko0414D"})]:
            if img.has_attr("alt") and img.has_attr("src"):
                tasks.append(fetch_data(img.get("src"), exdata=(img.get("alt"), img.get("src")),
                                        contentHandler=_download_img))

        if len(tasks) > 0:
            await asyncio.gather(*tasks)

    async def _handle_get_class(soup):
        for div in soup.find_all("div", attrs={"class": "listUrlBox"}):
            for a in div.find_all("a"):
                await fetch_data(f"{a.get('href')}", soupHandler=_handle_get_img)

    try:
        if not os.path.isdir(imgs_dir):
            os.mkdir(imgs_dir)

        await fetch_data(root_url, soupHandler=_handle_get_class)
    except BaseException as e:
        print(str(e))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())
