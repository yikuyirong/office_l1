import asyncio
import requests_async
from bs4 import BeautifulSoup

root_url = "http://db.jndjg.cn/"


async def _fetch_class1(retry=5):
    try:

        resp = await requests_async.get(root_url)
        await resp.close()

        soup = BeautifulSoup(resp.text, "html.parser")

        ul = soup.find("ul", attrs={"id": "firstMenu"})

        if ul:
            for a in ul.find_all("a"):
                print(1,a.text)
                await _fetch_class2(a.text, a.get("href"))
        else :
            raise Exception("未找到一类目录的ul元素")

    except BaseException as e:
        if retry > 0:
            await _fetch_class1(retry - 1)
        else:
            raise Exception(f"获取一类目录失败 {str(e)}")


async def _fetch_class2(title, url, retry=5):
    try:
        # print(title,url)
        resp = await requests_async.get(f"{root_url}{url}")
        await resp.close()

        soup = BeautifulSoup(resp.text, "html.parser")

        ul = soup.find_all("ul", attrs={"class": "menu scroll clickcontent"})[1]

        if ul:
            ass = ul.find_all("a")

            if len(ass) > 0:
                for a in ass:
                    print(2,title,a.text ,a.get("href"))
                    await _fetch_class3(f"{title} {a.text}",a.get("href"))
            else:
                pass


        else :
            raise Exception("未找到标记二类目录的nav元素")

    except BaseException as e:
        if retry > 0:
            await _fetch_class2(title, url, retry - 1)
        else:
            raise Exception(f"获取二类目录失败 {str(e)}")


async def _fetch_class3(title,url,retry = 5):
    try:
        # print(title,url)
        resp = await requests_async.get(f"{root_url}{url}")
        await resp.close()

        soup = BeautifulSoup(resp.text, "html.parser")

        nav = soup.find("nav", attrs={"id": "third_box"})

        if nav:
            for a in nav.find_all("a"):
                print(3,title, a.text,a.get("href"))
        else :
            raise Exception("未找到标记三类目录的nav元素")

    except BaseException as e:
        if retry > 0:
            await _fetch_class3(title, url, retry - 1)
        else:
            raise Exception(f"获取三类目录失败 {str(e)}")


async def _fetch_move(title, url,retry=5):
    try:
        # print(title,url)
        resp = await requests_async.get(f"{root_url}{url}")
        await resp.close()

        soup = BeautifulSoup(resp.text, "html.parser")

        nav = soup.find("nav", attrs={"id": "third_box"})

        if nav:
            for a in nav.find_all("a"):
                print(3,title, a.text,a.get("href"))
        else :
            raise Exception("未找到标记三类目录的nav元素")

    except BaseException as e:
        if retry > 0:
            await _fetch_class3(title, url, retry - 1)
        else:
            raise Exception(f"获取三类目录失败 {str(e)}")




async def main():
    await _fetch_class1()


if __name__ == '__main__':

    try:
        loop = asyncio.get_event_loop()

        loop.run_until_complete(main())

    except BaseException as e:
        print(f"\033[1;31m发生错误\033[0m  {str(e)}")
