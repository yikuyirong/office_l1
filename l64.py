import asyncio
import requests_async
from bs4 import BeautifulSoup


async def _fetch_weather():
    weather_url = "https://www.tianqi.com/jinan/7/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
        "Referer":weather_url
    }

    resp = await requests_async.get(weather_url ,headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")

        dl = soup.find("dl", attrs={"class": "table_day7 tbg"})

        if dl:
            print(dl.text)

    else:
        raise Exception(f"{resp.status_code} {resp.raise_for_status()}")


async def _send_email():
    pass


async def main():
    await _fetch_weather()

    await _send_email()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())
