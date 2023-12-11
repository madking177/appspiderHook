import requests

html = requests.get('https://91mjw.vip/vplay/MTgxLTQtMA==.html',
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', })

print(html.text)

exit()
r = requests.get('https://sod1.btycsw.com/20220302/J2dMrCW0/index.m3u8', headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
})

# print(r.text)

import re

for row in r.text.split('\n'):

    matchs = re.findall('http.*\.ts', row)
    # print(matchs)
    if len(matchs) > 0:
        print(matchs)
