from time import time
from urllib.request import Request, urlopen

urls=['https://www.google.co.kr/search?q=' + i for i in ['apple', 'pear','grape', 'pineapple', 'orange', 'strawberry']]

for line in urls:
      print(line)
begin = time()
result = []
for url in urls:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req)
    page = res.read()
    result.append(len(page))

print(result)
end = time()

print('실행시간: {0:.3f}초'.format(end-begin))