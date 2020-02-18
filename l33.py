
import asyncio

async def foo(i):

    await asyncio.sleep(0.1)

    return i

async def main():

    result = await asyncio.gather(*[foo(i) for i in range(20)])

    print(sum(result))


if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(main())






