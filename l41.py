import asyncio
from urllib import parse
import requests_async
import json


async def fetch():
    keyword = "吴佩慈"
    keyword = parse.quote(keyword)

    url = f"https://image.baidu.com/search/acjson?"


    params = {
        "tn": "resultjson_com",
        "ipn": "rj",
        "ct": "201326592",
        "is": "",
        "fp": "result",
        "queryWord": keyword,
        "cl": "2",
        "lm": "-1",
        "ie": "utf-8",
        "oe": "utf-8",
        "adpicid": "",
        "st": "-1",
        "z": "",
        "ic": "",
        "hd": "",
        "latest": "",
        "copyright": "",
        "word": keyword,
        "s": "",
        "se": "",
        "tab": "",
        "width": "",
        "height": "",
        "face": "0",
        "istype": "2",
        "qc": "",
        "nc": "1",
        "fr": "",
        "expermode": "",
        "force": "",
        "cg": "star",
        "pn": "30",
        "rn": "30",
        "gsm": "1e"
    }

    resp = await requests_async.get(url,params=params)

    if resp.status_code == 200:
        j = json.loads(resp.text)
        print(j)
    else:
        print(resp.status_code)


async def main():
    await fetch()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
