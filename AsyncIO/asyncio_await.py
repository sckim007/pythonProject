import asyncio

async def add(a, b):
    print('add: {0} + {1}'.format(a, b))
    await asyncio.sleep(1.0) # sleep 1 second
    return a + b

async def print_add(a, b):
    result = await add(a, b)
    print('print_add: {0} + {1}'.format(a, b))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_add(1, 2))
loop.close()
