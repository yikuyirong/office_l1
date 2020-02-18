
import asyncio
import urllib.parse
import requests_async
import json
import l60

async def _fetch_imgs(keyword):

    keyword = urllib.parse.quote(keyword)

    url = f"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&queryWord={keyword}&word={keyword}&pn=60&rn=122"

    resp = await requests_async.get(url)

    await resp.close()

    jdata = json.loads(resp.text)

    # print(len(jdata["data"]))
    print(jdata["data"][0:1])

    # for image in jdata["data"]:
    #     if image:
    #
    #         print(image)
    #         # l60.fetch_data()
    #
    #         print(image["middleURL"])



async def main():

    keyword = input("输入要检索的明星：")

    if not keyword:
        keyword = "吴佩慈"

    await _fetch_imgs(keyword)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())
