
import asyncio


L = []

async def producer(index):
    await asyncio.sleep(0.1)
    L.append(index)
    print("生产",index)
    await producer(index+1)

async def consumer():
    while True:
        await asyncio.sleep(0.1)
        if len(L) > 0:
            print("消费",L.pop(0))


async def main():

    await asyncio.gather(producer(1),consumer())


if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(main())










