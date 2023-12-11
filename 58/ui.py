# -*- coding: utf-8 -*-
import json

driver = None

import tools

from loguru import logger

from lxml import etree

headers = {
    'referer': 'https://58.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}
import traceback


def get_all_line_station(urls):
    all_station_name = []
    all_station_url = []
    for request_url in urls:
        response = tools.request_get(request_url)

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
    response = tools.request_get('https://bj.58.com/chuzu/sub/')
    for v in etree.HTML(response.text).xpath(
            '//div[@class="search_bd"]//dl[@class="secitem secitem_fist subway"]/dd/a'):
        subway_line_url = v.xpath('./@href')
        subway_line_name = v.xpath('./text()')
        if len(subway_line_name) > 0:
            if subway_line_name[0].find('不限') > -1:
                continue
            staion_name, station_url = get_all_line_station(subway_line_url)
            # print(staion_name, station_url)
            # exit()

            for each_staion_url in station_url:
                line_station_mercial_top3 = get_top_mercial_by_subway_station(each_staion_url)
                print({'url': each_staion_url, 'station': line_station_mercial_top3})
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
    response = tools.request_get(url)
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
    print(top_keys)  # 输出 ['e', 'd', 'c']

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
        print(response.text)
    return strip_data(data)


client = tools.get_chrome_client()
get_all_line()
