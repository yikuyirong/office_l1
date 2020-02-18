import asyncio
import re
from l35 import DownloadImage


class DownloadImage_Avlang(DownloadImage):

    def __init__(self):
        DownloadImage.__init__(self, root_url="http://av.avlang4.co/")

    def _get_img_dir(self):
        return f"avlang-fid-{self._fid}-images"

    def _get_list_page_url(self, page_index):
        return f"{self._root_url}thread-htm-fid-{self._fid}-page-{page_index}.html"

    def _get_img_uri(self, img):
        return img.get("src")

    def _check_a_is_valid(self, a):
        return a.has_attr("href") and \
               re.search(r"read-htm-tid-\d+(-fpage-\d+)?.html", a.get("href")) and \
               re.search("[a-zA-Z\u4e00-\u9fa5]+", a.text)

    def _check_img_is_valid(self, uri):
        return re.search(r"^http.+(\.jpg|\.png){1}$", uri)


class DownloadImage_Bssyw(DownloadImage):
    def __init__(self):
        DownloadImage.__init__(self, root_url="http://www.bssyw.com/bbs/")

    def _get_img_dir(self):
        return f"bssyw-fid-{self._fid}-images"

    def _get_list_page_url(self, page_index):
        return f"{self._root_url}thread.php?fid-{self._fid}-page-{page_index}.html"

    def _get_detail_page_pattern(self):
        return "read.php\?tid-\d+(-fpage-\d+)?.html"


class DownloadImage_Hszx(DownloadImage):
    def __init__(self):
        DownloadImage.__init__(self, root_url="http://bbs.voc.com.cn/")

    def _get_img_dir(self):
        return f"voc-{self._fid}-images"

    def _get_list_page_url(self, page_index):
        return f"{self._root_url}forum-{self._fid}-{page_index}.html"

    def _get_detail_page_pattern(self):
        return "topic-\d+-1-1.html"


class DownloadImage_Btshoufa(DownloadImage):
    def __init__(self):
        DownloadImage.__init__(self, root_url="http://btshoufa.cc/")

    def _get_img_dir(self):
        return f"btshoufa-{self._fid}-images"

    def _get_list_page_url(self, page_index):
        return f"{self._root_url}forum-{self._fid}-{page_index}.html"

    def _get_img_uri(self, img):
        return img.get("file")

    def _check_img_is_valid(self, uri):
        return "data.+jpg"

    def _check_a_is_valid(self, a):
        return a.has_attr("href") and a.has_attr("class") and \
               re.search("thread-\d+-1-\d+.html", a.get("href")) and \
               re.search("[a-zA-Z\u4e00-\u9fa5]+", a.text)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    # fid = None
    while True:
        fid = input("请输入要下载板块的fid：")
        if re.match("^\d+$", fid):
            fid = int(fid)
            break
        else:
            print("\033[1;31m请输入一个正整数\033[0m")


    def check_pages(value):
        pages = []

        for v in re.findall(r"[^,]+", value, re.S):
            if re.match(r"^\d+$", v):
                pages.append(int(v))

            if re.match(r"^\d+-\d+$", v):
                (begin, end) = map(lambda x: int(x), re.split("-", v))
                while begin <= end:
                    pages.append(begin)
                    begin = begin + 1

        return sorted(list(set(pages)))


    while True:
        pages = input("请输入下载的页[可使用,或-分割]：")

        pages = check_pages(pages)

        if len(pages) > 0:
            break
        else:
            print("\033[1;31m输入页数格式不对\033[0m")

    while True:
        cors = input("请输入并行下载数[100]：")
        if cors == "":
            cors = "100"

        if re.match("^\d+$", cors):
            cors = int(cors)
            break
        else:
            print("\033[1;31m请输入一个正整数\033[0m")

    try:
        # download = DownloadImage_Btshoufa()
        download = DownloadImage_Avlang()

        print(fid, pages, cors)

        loop.run_until_complete(download.dowload_images(fid, pages, cors))
    except BaseException as e:
        if not loop.is_closed():
            loop.close()

        print("\033[1;31m发生错误\033[0m", str(e))
