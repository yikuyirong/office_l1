
# import requests

import asyncio
import requests_async

async def main():

    # https://www.qpic.ws/images/2019/08/29/5B1P7.jpg
    resp = await requests_async.get("https://www.qpic.ws/images/2019/08/29/5B1P7.jpg")
    await resp.close()

    print(resp.status_code, resp.content)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

