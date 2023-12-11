import json
import time

from loguru import logger

proxy_ip = ''





def get_7890_proxy():
    proxies = {
        'http': f'http://127.0.0.1:7890',
        'https': f'http://127.0.0.1:7890',
    }
    return proxies


def get_user_agent():
    user_agents = '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.112 Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.111 Safari/537.3
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.111 Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.112 Safari/537.3
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.112 Safari/537'''.replace(
        '\r', '').split(
        '\n')
    randint = int(time.time()) % len(user_agents)
    logger.info({'randint': randint})
    return user_agents[randint]


remaining_ip = ''

import requests
from lxml import etree

import traceback

keywords = [
    'antibot/verifycode',
    '访问过于频繁，请登录后继续访问'
]


def requests_get(url):
    proxies = {}

    while True:
        response = requests.get(url=url, headers={'user-agent': get_user_agent()})
        # response = requests.get(url=url, headers={'user-agent': get_user_agent()}, proxies=proxies)
        logger.info({'验证码页面文案': etree.HTML(response.text).xpath('//p[@class="title"]/text()')})
        logger.info({'request': response.request.headers})
        logger.info({'response': response.headers})
        logger.info({'proxies': proxies})
        for keyword in keywords:
            if response.text.find(keyword) > -1 or response.status_code != 200:
                if keyword == 'antibot/verifycode':
                    logger.warning(response.text)
                logger.info({'命中': keyword})
                # proxies = get_proxyies(True)
                # update_proxy()
                time.sleep(2)
                break
        else:
            return response


def get_all_line_station(urls):
    all_station_name = []
    all_station_url = []
    for request_url in urls:
        response = requests_get(request_url)

        for v in etree.HTML(response.text).xpath('//div[@id="subStation"]/div[@id="sub_one"]/a'):
            subway_station_url = v.xpath('./@href')
            subway_station_name = v.xpath('./text()')
            if ''.join(subway_station_name).strip('\r\t\n ') == '不限':
                continue
            for vv in subway_station_url:
                all_station_url.append(vv)
            for vv in subway_station_name:
                all_station_name.append(vv)
    return all_station_name, all_station_url


def get_all_line():
    response = requests_get('https://hz.58.com/chuzu/sub/')
    for v in etree.HTML(response.text).xpath(
            '//div[@class="search_bd"]//dl[@class="secitem secitem_fist subway"]/dd/a'):
        subway_line_url = v.xpath('./@href')
        subway_line_name = v.xpath('./text()')
        if len(subway_line_name) > 0:
            if subway_line_name[0].find('不限') > -1:
                continue
            staion_name, station_url = get_all_line_station(subway_line_url)
            # logger.info(staion_name, station_url)
            # exit()

            if staion_name == '整条线路':
                continue
            for each_staion_url in station_url:
                line_station_mercial_top3 = get_top_mercial_by_subway_station(each_staion_url)
                logger.info({'url': each_staion_url, 'station': line_station_mercial_top3})
                if line_station_mercial_top3 is not None and line_station_mercial_top3["城市"] is not None:
                    with open(f'data/{line_station_mercial_top3["城市"][0]}.txt', 'a+') as f:
                        f.write('\n' + json.dumps(line_station_mercial_top3, ensure_ascii=False))


def strip_data(data):
    for k, v in data.items():
        if type(data[k]) == list:
            new_list = []
            for vv in data[k]:
                new_list.append(vv.__str__().strip('\r\t\n '))
            data[k] = new_list

    return data


def get_top_mercial_by_subway_station(url):
    response = requests_get(url)
    for v in etree.HTML(response.text).xpath('//span[@class="more-recommend"]/text()'):
        if v.find('该条件下房源较少，为您推荐') > -1:
            return
    keycount = dict()
    for item in etree.HTML(response.text).xpath('//div[@class="des"]//p[@class="infor"]'):
        name_concat = item.xpath('.//a/text()')
        if len(name_concat) > 1:
            if name_concat[0] not in keycount:
                keycount[name_concat[0]] = 0
            keycount[name_concat[0]] += 1

    # 将字典的值放入一个列表中
    values = list(keycount.values())

    # 对列表进行排序，获取最大值
    sorted_values = sorted(values, reverse=True)
    if len(sorted_values) > 3:
        # 获取排序后的列表的前三个元素
        top_three = sorted_values[:3]
    else:
        top_three = sorted_values
    top_keys = [key for key, value in keycount.items() if value in top_three]
    logger.info(top_keys)  # 输出 ['e', 'd', 'c']

    data = {
        '城市': etree.HTML(response.text).xpath('//div[@class="main-wrap"]//div[@class="nav-top-bar"]/a/text()'),
        '地铁线路': etree.HTML(response.text).xpath(
            '//div[@class="search_bd"]//dl[@class="secitem secitem_fist subway"]/dd/a[@class="select"]/text()'),
        '地铁站点': etree.HTML(response.text).xpath(
            '//div[@id="subStation"]/div[@id="sub_one"]/a[@class="select"]/text()'),
        '最高频次商圈': top_keys,
        '最高频次': top_three,
    }

    if len(data['城市']) == 0:
        logger.info(response.text)
    return strip_data(data)


get_all_line()
