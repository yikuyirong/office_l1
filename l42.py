import asyncio
import requests_async
from bs4 import BeautifulSoup

root_url = "http://www.jiabaoruye.com.cn"

urls = []


async def fetch_url(url=""):

    resp = await requests_async.get(f"{root_url}{url}")

    urls.append(url)

    if resp.status_code == 200:

        soup = BeautifulSoup(resp.text, "html.parser")

        for a in soup.find_all("a"):

            if a.has_attr("href"):

                suburl = a.get("href")

                if suburl.startswith("/") and suburl not in urls:

                    print(suburl)

                    await fetch_url(suburl)

    else:
        print("Error", resp.status_code, resp.raise_for_status())


async def main():
    await  fetch_url()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
