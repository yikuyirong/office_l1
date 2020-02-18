
import asyncio

async def child(delay):

    await asyncio.sleep(delay)

    print(f"Enter child {delay}")

    return "Child result"

async def main(loop):

    tasks = [child(1) for x in range(1,10) ]

    (cs,ps) = await asyncio.wait(tasks)

    for c in cs:
        print(c.result())



if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    except BaseException as e:
        loop.close()
        print("Found a exception",str(e))
        print(dir(e))








