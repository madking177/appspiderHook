# -*- coding: utf-8 -*-
from selenium.webdriver.common import by
from selenium.webdriver.chrome.options import Options
import selenium
import traceback
import time
import json
import datetime
from loguru import logger
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import by
import tkinter as tk
from tkinter import messagebox
from lxml import etree
from selenium import webdriver
import os
import web_auto
import tools

logpath = f'data/amazon_debug-{time.time()}.log'
if os.path.exists(logpath):
    os.remove(logpath)
logger.add(logpath)

check_box_label = ['搜索品牌']
driver = None

min_price = 3000
max_price = 20000
global_product_count_limit = 10
global_merchant_max_product_num = 3

amazon_url = 'https://www.amazon.co.jp'

product_output_data = 'data/产品输出数据.csv'
merchant_output_data = 'data/商铺输出数据.csv'
cateogry_output_data = 'data/门类输出数据.csv'
output_data_csv = 'data/output_v2.csv'

merchant_all_product_urls = []

start_url = 'https://www.amazon.co.jp/s?me=A36SEY84CVNONS&marketplaceID=A1VC38T7YXB528'
headers = ['asin', '品牌', '产品名称', '价格', '卖家', '卖家数量', 'url', ]

# 抓取第N商户
global_merchant_index = 0
# 抓取第N商品
global_product_detail_index = 0
# 门类翻页
global_category_page_index = 0

mode_category = 'category'
mode_product = 'product'
mode_merchant = 'merchant'

import time
import string
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def extract_english_japanese(text):
    pattern = r'[\u4e00-\u9faf\u3040-\u309f\u30a0-\u30ff]+|[a-zA-Z]+'
    matches = re.findall(pattern, text)
    if len(matches) == 0:
        return ''
    else:
        return ' '.join(matches)


def extract_product_id_from_url(ab_url):
    product_ids = re.findall('/dp/.*/ref=', ab_url)
    if len(product_ids) > 0:
        return product_ids[0]
    else:
        return ''


def enter_merchant():
    global global_merchant_index
    driver.find_element(by.By.XPATH, '//div[@id="seller-info-storefront-link"]//span/a').click()
    global_merchant_index += 1
    logger.info(f'进入 {global_merchant_index} 家商铺 ')


def extract_all_product_url_from_merchant(start_url: str, limit=False) -> list:
    '''
    给一个商铺的url 拿到所有产品的url
    '''

    urls_ok_all = []
    global drivertuichu1
    driver = get_chrome_driver()

    if start_url.strip('\r\t\n') == '':
        return None
    page_index = 0
    logger.info(
        json.dumps({"info": "通过商户获取产品", "url": start_url.strip('\n'), 'index': global_product_detail_index},
                   ensure_ascii=False))
    driver_get(start_url)
    enter_links = etree.HTML(driver.page_source).xpath('//div[@id="seller-info-storefront-link"]//span/a')
    if len(enter_links) > 0:
        enter_merchant()

    if driver.page_source.find('キーワードが正しく入力されていても一致する商品がない場合は、別の言葉をお試しください。') > -1:
        logger.error('商铺有问题 提前退出')

        return None

    get_null_product_info_times = 0
    while 1:
        els = etree.HTML(driver.page_source)

        urls_ok = []
        rows = els.xpath('//div[@class="a-section"]')
        for row in rows:
            prodct_urls = row.xpath(
                './/div[@class="a-section a-spacing-small a-spacing-top-small"]/div/h2/a/@href')
            row_price = row.xpath(
                './/span[@class="a-price"]//text()')
            # print(row_price)
            # if len(prodct_urls)==0 and len(row_price)==0:

            logger.info({'urls': prodct_urls, 'row_price': row_price, })
            if len(row_price) > 0:
                row_price = ''.join(re.findall('[0-9]{1,}', row_price[0]))
                row_price = int(row_price)
                if row_price >= min_price and row_price <= max_price and len(prodct_urls) > 0:
                    urls_ok.append(prodct_urls[0].__str__())
                    urls_ok_all.append(get_url(prodct_urls[0].__str__()))
        if len(urls_ok_all) > global_product_count_limit:
            logger.warning({'事件': f'抓取总数:{len(urls_ok_all)} 用户设置总数{global_product_count_limit}'})
            return urls_ok_all
        logger.info(json.dumps(
            {"本商铺累计抓取数": len(urls_ok_all), '本页抓取数': len(urls_ok), "页": page_index, 'min_price': min_price,
             'max_price': max_price}, ensure_ascii=False))
        if len(urls_ok) == 0:
            get_null_product_info_times += 1
            if get_null_product_info_times >= 3:
                logger.error('抓取抓取商铺都是空')
                break
        else:
            get_null_product_info_times = 0

        # 插入代码 是否限制某个店铺的商品
        if limit:
            if len(urls_ok_all) > global_merchant_max_product_num:
                logger.info(f'满足商铺最大抓取数 {global_merchant_max_product_num} 进入下一个商铺')
                urls_ok_all = urls_ok_all[:global_merchant_max_product_num]
                break

        # 是否翻页
        page_urls = els.xpath(
            '//span[@class="s-pagination-strip"]//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href')
        if len(page_urls) == 0:
            logger.info('本店铺产品url采集结束')
            break
        elif len(page_urls) > 0:
            start_url = amazon_url + page_urls[0]
            driver_get(start_url)
            page_index += 1
    return urls_ok_all


# 从目录提取商品


def extract_list_by_category(html):
    global min_price, max_price
    global global_count
    all_price = []
    l = etree.HTML(html)
    urls_oks = []
    for v in l.xpath('//div[@data-component-type="s-search-result"]//div[@class="sg-col-inner"]'):
        url = v.xpath(
            './/h2/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href')
        price = v.xpath('.//span[@class="a-price"]//span[@class="a-price-whole"]/text()')
        deliver = v.xpath('.//div[@class="a-row"]/span/span[@class="a-color-base"]/text()')
        # logger.debug([price, deliver])
        deliver = ''.join(deliver).lower()
        # print(deliver)
        if deliver.find('amazon') > -1 or deliver.find('亚马') > -1:
            logger.error('不需要亚马逊的数据')
            continue
        # print([url, price, deliver])

        # 这块价格很多低于预期 xpath表达式没问题
        if len(url) >= 1 and len(price) >= 1:
            price = ''.join(re.findall('[0-9]{1,}', price[0]))
            if price != '':
                price = int(price)
                if price >= min_price and price <= max_price:
                    all_price.append(price)
                    urls_oks.append(url[0])
                    global_count += 1
    logger.info(json.dumps({
        "产品数量": len(urls_oks),
        "最高价": max_price,
        "最低价": min_price,
        "页码": global_category_page_index,
        "价格": all_price,
    }, ensure_ascii=False))

    return urls_oks


def category_product(category_url):
    global driver
    all_product_urls = []
    global min_price, max_price, crwal_count
    global global_count, write_product
    global global_category_page_index
    global_count = 0
    driver = get_chrome_driver()

    category_urls = [category_url]
    print(category_urls)
    for url in category_urls:
        print('开始亚马逊抓取', url)
        driver_get(url)
        hits = driver.find_elements(by.By.XPATH, '//li/span/a[@class="a-link-normal a-color-tertiary"]')
        if len(hits) == 0:
            print('没有可以提取的门类信息 错误！！')
            exit()
        else:
            hits[len(hits) - 1].click()
            driver.find_element(by.By.XPATH, '//a[@id="apb-desktop-browse-search-see-all"]').click()
            while 1:
                global_category_page_index += 1
                try:
                    product_list = extract_list_by_category(driver.page_source)
                    for product_url in product_list:
                        all_product_urls.append(product_url)
                except:
                    traceback.print_exc()
                next = etree.HTML(driver.page_source).xpath(
                    '//span[@class="s-pagination-strip"]//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href')
                if len(next) >= 1:
                    next = amazon_url + next[0]
                    driver_get(next)

                    logger.info({'累计数量': len(all_product_urls), 'limit_count': global_product_count_limit})

                    if len(all_product_urls) > global_product_count_limit:
                        logger.warning({
                            '事件': f'门类到商品 总数{len(all_product_urls)} 抓取结束 用户设置总数{global_product_count_limit}'
                        })
                        return all_product_urls
                else:
                    print(f'门类抓取完毕 共计{global_count}')
                    return all_product_urls
    return all_product_urls


def task_product(start_url):
    logger.warning('开始采集商品')
    # 通过产品找商铺 通过商铺找产品
    product_merchant_product(start_url)

    logger.warning('开始采集品牌')
    # 搜索品牌 只要no result的
    no_result_brand = search_brand(product_output_data)

    logger.warning('输出文件')
    json_to_csv(no_result_brand, method=mode_product, output=product_output_data)


def task_merchant(start_url):
    with open(merchant_output_data, 'w+', encoding='utf8') as merchant_file:
        merchant_file.write(','.join(headers) + '\n')
        error = 0
        while 1:
            product_urls = extract_all_product_url_from_merchant(start_url)
            if product_urls is None:
                error += 1
                if error > 5:
                    raise "重试五次抓商铺都失败"
            else:
                break
        datas = []
        driver = get_chrome_driver()
        index = 0
        # 得到产品列表
        for product_url in product_urls:
            index += 1
            driver_get(get_url(product_url))
            r = scan_product_detail(driver, False)
            data = r['product']
            if data is not None:
                datas.append(data)
                merchant_file.write(tools.extract_product_info(data) + '\n')
                merchant_file.flush()
            logger.info(data)
            logger.info(
                {'进度': global_product_detail_index, '总数': global_product_count_limit, 'product_url': product_url, })

    no_result_brand = search_brand(merchant_output_data)
    json_to_csv(no_result_brand, method=mode_merchant, output=merchant_output_data)


# 门类获取商品任务
def task_category(start_url):
    with open(cateogry_output_data, 'w+', encoding='utf8') as category_file:
        category_file.write(','.join(headers) + '\n')
        all_product_urls = category_product(start_url)
        datas = []
        driver = get_chrome_driver()
        product_detail_index = 0

        product_ids = set()
        # 产品url去重
        all_unique_product_id = []
        for product in all_product_urls:
            id = extract_product_id_from_url(product)
            if id not in product_ids or id == '':
                product_ids.add(id)
                all_unique_product_id.append(product)
            else:
                logger.error({
                    '事件': '商品id重复',
                    'id': id,
                })
            # logger.info({'id': id, 'url': product, })
        logger.info(
            {'事件': '去重', '商品去重之前': len(all_product_urls), '商品去重之后': len(all_unique_product_id), })
        for product_url in all_unique_product_id:
            product_detail_index += 1
            product_url = get_url(product_url)
            driver_get(get_url(product_url))
            # 得到data
            r = scan_product_detail(driver, False)
            data = r['product']
            if data is not None:
                datas.append(data)
                w = tools.extract_product_info(data) + '\n'
                logger.info(w)
                category_file.write(w)
            logger.info({'进度': product_detail_index, "总数": global_product_count_limit, 'product_url': product_url})

            if product_detail_index > global_product_count_limit:
                logger.warning('category 详情点击次数已经满足需求 所以退出抓取')
                break
    search_brand(cateogry_output_data)
    json_to_csv(method=mode_category)


# 输入brand是空的话 从文件读
# 第二个参数是模式
# 第三个参数是输出
def json_to_csv(no_result_brand=[], method='', output=''):
    if checkbox_values[0].get():
        if len(no_result_brand) == 0:
            with open('data/no_result.txt', encoding='utf8') as r:
                for brand in r.read().split('\n'):
                    no_result_brand.append(brand)
    else:
        no_result_brand = ['']
    logger.info({'可用品牌': no_result_brand})

    if output == '':
        if method == mode_merchant:
            output = merchant_output_data
        if method == mode_category:
            output = cateogry_output_data
        if method == mode_product:
            output = product_output_data

    with open(output, mode='r', encoding='utf8') as r:
        datas = r.read().split('\n')[1:]

    file_name = f"data/output-{method}-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    with open(file_name, mode='wb+') as target_file:
        target_file.write((','.join(headers)).encode())
        for read_row in datas:
            cells = read_row.split(',')
            if len(cells) == 7:
                product_id = cells[0].strip('\r\t\n ')
                brand_name = cells[1].strip('\r\t\n ')
                product_name = cells[2].strip('\r\t\n ')
                product_price = cells[3].strip('\r\t\n ')
                seller = cells[4].strip('\r\t\n ')
                seller_num = cells[5].strip('\r\t\n ')
                product_url = cells[6].strip('\r\t\n ')
                # 1
                if product_id == '':
                    logger.error('ASIN ERROR')

                # 2
                brand_ok = False
                for no_result in no_result_brand:
                    if brand_name.find(no_result) > -1:
                        brand_ok = True
                if not brand_ok:
                    logger.error('不需要的品牌')
                    continue
                # 3
                if product_name == '':
                    logger.error('product_name error')
                    continue

                price_array = ''.join(re.findall('[0-9]{1,}', product_price))
                if len(price_array) > 0:
                    # 4
                    price = int(price_array)
                else:
                    price = 0

                if price <= min_price and price >= max_price:
                    logger.error('价格不合法')
                    continue
                if seller == '':
                    logger.error('卖家名称错误')
                    continue
                if int(seller_num) < 3:
                    logger.error('关联卖家数量错误')
                    continue

                target_file.write(f"\n{read_row}".encode())
                target_file.flush()
    logger.warning({'输出结果': file_name, })


def extract_product_detail_info(html, current_url=''):
    seller_num = 0
    dom_tree = etree.HTML(html)

    new_asin = ''
    v = dom_tree.xpath('//div[@id="prodDetails"]//text()')
    # logger.info(v)
    asin_detect = False
    for text in v:
        if text.find('ASIN') > -1:
            asin_detect = True
        if asin_detect:
            hits = re.findall('[0-9A-Z]{10}', text)
            if len(hits) > 0:
                new_asin = hits[0]
                break

    if new_asin == '':
        asin_detect = False

        v = dom_tree.xpath('//div[@id="detailBullets_feature_div"]//span/text()')
        # logger.info(v)
        for text in v:
            if text.find('ASIN') > -1:
                asin_detect = True
            if asin_detect:
                hits = re.findall('[0-9A-Z]{10}', text)
                if len(hits) > 0:
                    new_asin = hits[0]
                    break

    brand = dom_tree.xpath('//a[@id="bylineInfo"]/text()')
    if len(brand) > 0:
        brand = brand[0]
    else:
        brand = ''
    for t in dom_tree.xpath('//a/div[@class="a-box-inner"]/div[@class="olp-text-box"]/span//text()'):
        if t.find('出品') > -1:
            seller_num = re.findall('[0-9]{1,}', t)[0].strip('\r\t\n ')
    name = dom_tree.xpath('//span[@id="productTitle"]//text()')
    if len(name) == 0:
        name = ''
    else:
        name = name[0]
    name = name.strip('\r\n\t ')

    price_array = dom_tree.xpath('//div[@id="corePriceDisplay_desktop_feature_div"]//div//span/text()')

    new_price = ''
    for price in price_array:
        price = price.strip('\r\t\n ')
        price_match = re.findall('[0-9]{1,}', price)
        if len(price_match) > 0:
            price = ''.join(price_match)
            price = int(price)
            if price > 3000 and price < 20000:
                new_price = price
    merchant = dom_tree.xpath('//a[@id="sellerProfileTriggerId"]//text()')
    # logger.info(merchant)
    new_merchant = ''
    for v in merchant:
        if len(v.strip(' \r\t\n')) > 0:
            new_merchant = v
    if new_merchant == '':
        vv = dom_tree.xpath('//div[@tabular-attribute-name="販売元"]//a//text()')
        logger.info(vv)
        for vvv in vv:
            if len(vvv) > 0:
                new_merchant = vvv
    if new_merchant.lower().find('amazon') > -1:
        return None
    hit_words = dom_tree.xpath('//div[@id="icon-farm-container"]//div[@data-cel-widget="DELIVERY_JP"]//text()')
    if ''.join(hit_words).lower().find('amazon') > -1:
        logger.error('amazon')
        return None
    data = {
        'asin': new_asin,
        '品牌': brand,
        '产品名称': name,
        '价格': new_price,
        '卖家': new_merchant,
        '卖家数量': seller_num,
        'url': current_url,
    }
    return data


def scan_product_detail(driver: selenium.webdriver.chrome, right=True):
    try:
        global global_product_detail_index
        wait(0.2)
        product_data = extract_product_detail_info(driver.page_source, driver.current_url)
        merchant_urls = []
        global_product_detail_index += 1

        if right:
            right_hits = etree.HTML(driver.page_source).xpath('//div[@id="olpLinkWidget_feature_div"]//a')
            # 判断右侧是否有按钮
            if len(right_hits) > 0:
                try:
                    driver.find_element(by.By.XPATH, '//div[@id="olpLinkWidget_feature_div"]//a').click()
                    for e in driver.find_elements(by.By.XPATH,
                                                  '//div[@class="a-fixed-left-grid-col a-col-right"]//a[@role="link"]'):
                        merchant_urls.append(e.get_property('href'))
                    if len(merchant_urls) >= 4:
                        logger.info('清除第一个商铺 最后一个商铺 抓取中间商铺信息')
                        merchant_urls = merchant_urls[1:-1]

                    logger.info({
                        '详情页点击数': global_product_detail_index,
                        '关联商户数': len(merchant_urls), })

                except:
                    traceback.print_exc()
            else:
                logger.info('右侧没有可点击按钮')

        if driver.page_source.find('Amazonによる発送') > -1 or driver.page_source.find('亚马逊配送') > -1:
            logger.error('亚马逊')
            product_data = None

        if product_data is None:
            return {
                'product': product_data,
                'merchant_urls': merchant_urls,
            }
        product_data = json.dumps(product_data, ensure_ascii=False)

        return {
            'product': product_data,
            'merchant_urls': merchant_urls,
        }
    except:
        traceback.print_exc()
        return {
            'product': None,
            'merchant_urls': []
        }


def scan_product_urls_list(urls):
    driver = get_chrome_driver()
    for product_url in urls:
        scan_product_detail(driver, False)


def product_merchant_product(start_url):
    with open(product_output_data, 'w+', encoding='utf8') as product_file:
        product_file.write(','.join(headers) + '\n')
        product_list = []
        merchant_list = []
        logger.info('通过产品找商铺 通过商铺找产品')
        global write_merchant, write_output, index
        index = 0
        driver = get_chrome_driver()
        product_list.append(start_url)

        datas = []

        all_product_id = []
        loop_times = 10
        all_sellers = []

        for loop_index in range(loop_times):  # 循环九个周期
            logger.info(f'第{loop_index}轮产品 商铺队列抓取')
            product_list = list(set(product_list))

            logger.warning(f'共计产品{len(product_list)}')
            # 产品队列抓取
            for product_url in product_list:

                if product_url.startswith('http'):
                    ab_url = product_url
                else:
                    ab_url = amazon_url + product_url

                product_ids = re.findall('/dp/.*/ref=', ab_url)

                for product_id in product_ids:
                    if product_id in all_product_id:
                        print('已经抓取 跳过')
                        continue
                    else:
                        all_product_id.append(product_id)
                if global_product_detail_index > global_product_count_limit:
                    logger.warning('商品-店铺采集模式已经结束 全局点击数已经大于用户设置最大数量')
                    break
                print(f"- {ab_url}")
                driver_get(ab_url)
                data = scan_product_detail(driver)
                if data is None:
                    continue

                logger.info(data['product'])
                logger.info({
                    '进度': global_product_detail_index,
                    '总数': global_product_count_limit,
                    '产品id': product_ids,
                    '本轮需抓取': len(product_list),
                    '产品关联商户': len(data['merchant_urls']),
                    '轮数': loop_index,
                })
                merchants_urls, product = data['merchant_urls'], data['product']
                if data['product'] is not None:
                    datas.append(product)
                    product_file.write(tools.extract_product_info(data) + '\n')
                    product_file.flush()
                for merchant_url in merchants_urls:
                    merchant_list.append(merchant_url)

            product_list = []

            logger.info('商铺抓取 产品补充')

            merchant_list = list(set(merchant_list))

            merchant_list_v2 = []
            for v in merchant_list:
                for val in v.split('&'):
                    if val.find('seller') > -1:
                        if val in all_sellers:
                            pass
                        else:
                            logger.info({'event': '新增关联商户', '商户id': f'{val}'})
                            all_sellers.append(val)
                            merchant_list_v2.append(v)

            logger.warning({
                'event': '本轮商品抓取结束  开始采集关联商户',
                '整体已经抓取商铺': len(all_sellers),
                '未去重商户': len(merchant_list),
                '去重商户': len(merchant_list_v2),
                '轮数': loop_index,
            })

            # 商家队列补充产品队列
            for merchant_url in merchant_list_v2:
                if merchant_url.startswith('http'):
                    # 通过商铺获得所有产品
                    all_product = extract_all_product_url_from_merchant(merchant_url, True)
                    if all_product is not None:
                        for product_url in all_product:
                            product_list.append(product_url)
                else:
                    # 通过商铺获得所有产品
                    all_product = extract_all_product_url_from_merchant(amazon_url + merchant_url, True)
                    if all_product is not None:
                        for product_url in all_product:
                            product_list.append(product_url)

                if len(product_list) + len(all_product_id) > global_product_count_limit:
                    logger.info('数量已经足够 退出商铺采集的逻辑')
                    break

            merchant_list = []


def search_brand(output):
    # 默认不搜索品牌
    if not checkbox_values[0].get():
        return []
    driver = get_chrome_driver()
    datas = []
    with open(output, 'r', encoding='utf8') as f:
        brands = []
        for row in f:
            if row.strip('\r\t\n ') == '':
                continue
            try:
                data = json.loads(row)
                cuts = data['品牌'].split(':')
                if len(cuts) >= 2:
                    data['品牌'] = cuts[1]
                brands.append(data['品牌'])
                datas.append(data)
            except Exception as e:
                traceback.print_exc()

        brands = list(set(brands))

        logger.info(brands)
        logger.info({'length': len(brands)})
        brand_no_result = []
        index = 0
        for brand_text in brands:
            index += 1
            brand_text = extract_english_japanese(brand_text)
            try:
                brand_text = brand_text.strip('\r\t\n')
                if brand_text == '':
                    continue
                driver_get('https://branddb.wipo.int/')
                driver.find_element(by.By.XPATH,
                                    '//w-input-autocomplete[@data-test-id="inputSearch"]//input').send_keys(brand_text)

                driver.find_element(by.By.XPATH, '//button[@data-test-id="btnSearch"]').click()
                time.sleep(0.3)
                while 1:
                    if driver.page_source.find('Loading...') > -1:
                        continue
                    else:
                        break
                time.sleep(0.3)
                error = driver.page_source.find('search_error')
                error_no_result = driver.page_source.find('No results found!')

                no_result_logic = error_no_result > -1 or error > -1
                if no_result_logic:
                    print(f'no result:{brand_text}')
                    brand_no_result.append(brand_text)

                logger.info({
                    '序号': index,
                    '品牌': brand_text,
                    '需查询总数': len(brands),
                    '查询无': error_no_result,
                    '报错': error,
                    '需要': no_result_logic,
                })

            except Exception as e:
                traceback.print_exc()

    with open('data/no_result.txt', 'w+', encoding='utf8') as f:
        f.write('\n'.join(brand_no_result))

    return brand_no_result


def wait(sec: float = 1.0):
    logger.info(f'等待 {sec} 秒')
    time.sleep(sec)


def driver_get(url):
    # 每次访问前做一次验证码检查
    global driver
    refresh = 0
    while 1:
        try:
            driver.get(url)
            if driver.page_source.find('この画像に見える文字を入力してください:') > -1 or refresh > 5:
                driver.get(amazon_url)
                driver.get('https://myip.ipip.net/')
                driver.get(url)
            if driver.page_source.find('无法访问此网站') > -1:
                driver.refresh()
                refresh += 1
            else:
                break
        except:
            traceback.print_exc()
            driver = web_auto.get_chrome_driver()
            logger.error('浏览器奔溃 考虑是否重启浏览器')
    # 禁用了js


def get_chrome_driver() -> webdriver.Chrome:
    global driver
    if driver is None:
        driver = web_auto.get_chrome_client()

    return driver


def get_url(url: str):
    if url.startswith('http'):
        return url
    else:
        return amazon_url + url


def event_action():
    global global_product_count_limit, global_merchant_max_product_num
    for index in range(len(check_box_label)):
        print(check_box_label[index], checkbox_values[index].get())

    v_category = entries[0].get()
    v_product = entries[1].get()
    v_seller = entries[2].get()
    v_min_price = entries[3].get()
    v_max_price = entries[4].get()
    v_crawl_num = entries[5].get()
    merchant_max_limit = entries[6].get()
    if merchant_max_limit == '':
        global_merchant_max_product_num = 100
    else:
        global_merchant_max_product_num = int(merchant_max_limit)
    if v_min_price > '':
        v_min_price = int(v_min_price)
    else:
        v_min_price = 0

    if v_max_price > '':
        v_max_price = int(v_max_price)
    else:
        v_max_price = 0

    if v_crawl_num > '':
        v_crawl_num = int(v_crawl_num)
    else:
        v_crawl_num = 0
    if v_min_price > v_max_price:
        messagebox.showinfo(title='', message='价格错误')

    # 最小价格
    if v_min_price < 3000:
        v_min_price = 3000
    elif v_min_price > 20000:
        v_min_price = 3000
    # 最高价格
    if v_max_price < 3000:
        v_max_price = 20000
    elif v_max_price > 20000:
        v_max_price = 20000

    # 抓取数量
    if v_crawl_num < 1:
        v_crawl_num = global_product_count_limit
    elif v_crawl_num > 10000:
        v_crawl_num = global_product_count_limit

    url_count = 0
    start_url = ''
    if v_category > '':
        url_count += 1
        start_url = v_category
    if v_product > '':
        url_count += 1
        start_url = v_product
    if v_seller > '':
        url_count += 1
        start_url = v_seller

    if url_count == 1:
        try:
            global min_price, max_price

            min_price = v_min_price
            max_price = v_max_price

            global_product_count_limit = v_crawl_num
            messagebox.showinfo(title='提示', message='抓取任务创建成功')
            logger.info(f'开始url {start_url}')
            logger.info(f'最低价{v_min_price}')
            logger.info(f'最高价{v_max_price}')
            logger.info(f'抓取数量{v_crawl_num}')

            start_url = start_url.strip('\r\t\n ')
            if v_category > '':
                task_category(start_url)
            if v_product > '':
                task_product(start_url)
            if v_seller > '':
                task_merchant(start_url)
            logger.warning('抓取完毕 自动退出')
        except:
            traceback.print_exc()

            input('抓取错误 请看日志 回车键退出')

            if driver is not None:
                driver.close()
                driver.quit()

        if driver is not None:
            driver.close()
            driver.quit()
        # messagebox.showinfo('success', '任务成功 退出任务')

    else:
        messagebox.showinfo('warning', '兄弟 你给的入口链接有问题 url入口只能填写一个')


root = tk.Tk()
root.geometry("600x600")
root.resizable(False, False)
entries = []
checkbox_values = []
for label in check_box_label:
    checkbox_values.append(tk.BooleanVar())


def events():
    try:
        event_action()
    except Exception as e:
        # messagebox.showinfo('error', '执行异常 请看日志')
        traceback.print_exc()
        logger.exception(e)
    logger.stop()
    exit()


def create_ui():
    if not os.path.exists('data'):
        os.mkdir('data')
    for text in ['类目url', '产品url', '店铺url', f'最低价({min_price}-{max_price})',
                 f'最高价({min_price}-{max_price})', f'采集数量(1-{global_product_count_limit})',
                 f"商铺限制采集数量({global_merchant_max_product_num})"]:
        label = tk.Label(root, text=text)
        label.pack()
        entry = tk.Entry(root)
        entry.pack()
        entries.append(entry)
    for i, text in enumerate(check_box_label):
        checkbox = tk.Checkbutton(root, text=text, variable=checkbox_values[i])
        checkbox.pack()

    button = tk.Button(root, text="确定", command=events)
    button.pack()
    root.mainloop()


create_ui()
