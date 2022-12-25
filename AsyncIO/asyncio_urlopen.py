import asyncio
from time import time
from urllib.request import Request, urlopen

urls=['https://www.google.co.kr/search?q=' + i for i in ['apple', 'pear','grape', 'pineapple', 'orange', 'strawberry']]


async def fetch(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = await loop.run_in_executor(None, urlopen, req)
    page = await loop.run_in_executor(None, res.read)
    return len(page)


async def main():
    futures = [asyncio.ensure_future(fetch(url)) for url in urls]
    result = await asyncio.gather(*futures)
    print(result)


begin = time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
end = time()

print('실행시간: {0:.3f}초'.format(end-begin))