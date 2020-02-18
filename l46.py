import asyncio
import requests_async
import os
import PyPDF2
from PIL import Image

download_dir = "EnglishPEP_6"


async def _download_imgs():
    await asyncio.gather(
        *[_download_img(x, f"http://bp.pep.com.cn/ebooks/yypepliunjxc/files/mobile/{x}.jpg?200201121645") for x in
          range(1, 77)])

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
    resp = await requests_async.get(url)

    if resp.status_code == 200:

        name = "%03d" % index

        f = open(os.path.join(download_dir, f"{name}.jpg"), "wb")
        f.write(resp.content)
        Image.open(f.name).save(os.path.join(download_dir, f"{name}.pdf"), "PDF")
        f.close()
        os.remove(f.name)

        print("下载完成", index, url)


if __name__ == "__main__":

    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)

    asyncio.get_event_loop().run_until_complete(_download_imgs())
