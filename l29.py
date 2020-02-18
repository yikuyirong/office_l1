import asyncio


async def foo(value):
    await asyncio.sleep(0.1)
    print(value)


async def main():
    L = list(range(1000, 1345))

    i = 0

    while i < len(L):
        print(i,min(len(L), i + 10),len(L))
        await asyncio.gather(*[foo(t) for t in L[i: min(len(L), i + 10)]])
        i = i + 10


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except:
        loop.close()
