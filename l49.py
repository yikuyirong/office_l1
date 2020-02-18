import asyncio
from bs4 import BeautifulSoup
import requests_async
import re


async def _fetch_shici():
    url = "http://www.shicimingju.com/chaxun/zuozhe/91.html"

    resp = await requests_async.get(url)

    if resp.status_code == 200:

        soup = BeautifulSoup(resp.text, "html.parser")

        for div in soup.find_all("div", attrs={"class": "shici_list_main"}):
            print("#" + "_".join([x for x in re.split("[\s，。：;“”？！《》]+", div.text) if x and x != "展开全文" and x != "收起"]))


async def main():
    await _fetch_shici()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
