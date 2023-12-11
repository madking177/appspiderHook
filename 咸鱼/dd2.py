# -*- coding: utf-8 -*-
import json
import os
import io
import sys
import time
from dd import send_dingding

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 改变标准输出的默认编码
with open('output.txt', mode='r', encoding='utf-8') as f:
    text = json.loads(f.read())

for v in text['data']['resultList']:
    publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
        int(v['data']['item']['main']['clickParam']['args']['publishTime']) / 1000))
    ts = ''
    for other_info in json.loads(v['data']['item']['main']['clickParam']['args']['serviceUtParams']):
        if other_info['args']['content'].find('发布') > -1:
            ts = other_info['args']['content']

    data = {
        'desc': v['data']['item']['main']['exContent']['detailParams']['title'],
        'item_id': v['data']['item']['main']['exContent']['dislikeFeedback']['clickParam']['args']['itemId'],
        'pic': v['data']['item']['main']['exContent']['picUrl'],
        'publish_time': publish_time,
        'ts': ts,
        'price': v['data']['item']['main']['exContent']['detailParams']['soldPrice']
    }
    # print(data)

    send_dingding(data['desc'], data['ts'], data['item_id'], data['pic'], data['price'])
