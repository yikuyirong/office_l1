import asyncio
from bs4 import BeautifulSoup
import requests
import re


async def _get_shici(index):
    url = f"http://www.zggdwx.com/qianjiashi/{index}.html"

    with requests.get(url) as resp:

        if (resp.status_code == 200):

            soup = BeautifulSoup(resp.text, "html.parser")

            title = soup.find("h2", attrs={"class": "subname"})

            while title:
                author = title.find_next("p", attrs={"class", "subauther"})
                if author:
                    content = author.find_next("blockquote")
                    if content:
                        author = "_".join(re.findall(r'[^（）\s]+', author.text, re.S))
                        content = "_".join(re.findall(r'[^，。\s]+', content.text, re.S))

                        text = f"{title.text}_{author}_{content}"

                        print(text)


                    else:
                        continue
                else:
                    continue

                title = title.find_next("h2", attrs={"class": "subname"})

            # for content in soup.find_all("h2",{"class":"subname"}):
            #     print(content.text)


async def main(*indexs):
    for index in indexs:
        await _get_shici(index)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main(1,2,3,4))
    except:
        loop.close()
