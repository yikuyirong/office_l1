

import asyncio

async def sayHello(delay):

    await asyncio.sleep(delay)

    print(delay)

    return delay


async def main(el):
    print("Begin")

    tasks = [sayHello(1),sayHello(2),sayHello(3)]

    (complete,pending) = await asyncio.wait(tasks)

    print([t.result() for t in complete])

    print("End")


el = asyncio.get_event_loop()

el.run_until_complete(main(el))
