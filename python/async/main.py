import asyncio
async def delay(duration):
    print(f'sleep for {duration} sec')
    await asyncio.sleep(duration)
    print(f'sleeped for {duration} sec')

async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    await sleep_for_three
    await sleep_again
asyncio.run(main())
