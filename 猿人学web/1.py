import json

import execjs, time

t = time.time()
with open('1-3-window-b-source-code.js') as f:
    js = execjs.compile(f.read())

t1 = int(time.time() + 100000) * 1000
print(t1)
t2 = int(t1 / 1000)
m1 = js.call('token_v1', t1)
import requests

count = 0
times = 0
for page in range(1, 6):
    url = f'https://match.yuanrenxue.cn/api/match/1?page={page}&m={m1}%E4%B8%A8{t2}'
    print({'fake': url, })
    response = requests.get(url)
    print(response.text)
    data = json.loads(response.text)
    for v in data['data']:
        print(v['value'])
        count += v['value']
        times += 1

print({'总金额': count, '次数': times, '平均值': count / times})
