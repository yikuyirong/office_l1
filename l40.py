
import asyncio

async def foo(retry = 5):

    try:

        print(f"Start {retry}")

        await asyncio.sleep(0.1 * retry)

        raise Exception(f"E{retry}")

    except Exception as e:
        if retry > 0:
            await  foo(retry - 1)
        else:
            print(str(e))

if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(foo(10))






