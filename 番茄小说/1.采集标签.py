# -*- coding: utf-8 -*-
# 1.导入appium
import json
import time
import traceback
from lxml import etree

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from typing import List
from loguru import logger
from data import fq

driver: webdriver.webdriver.WebDriver


def bind_device(device_name: str):
    # 每个进程单独控制一个driver去操作amulator设备
    global driver, explicit_wait
    # 2.添加启动参数
    # 就是Desired capabilities，是一个字典类型的对象。
    desired_caps = {
        "platformName": "Android",  # 系统名称
        "platformVersion": "9",  # 系统版本
        # "deviceName": "emulator-5554",  # 设备名称
        # "udid": "emulator-5554",  # 设备名称
        "deviceName": device_name,  # 设备名称
        "udid": device_name,  # 设备名称
        # "appPackage": "com.android.settings",  # APP包名
        # "appActivity": ".Settings",  # APP启动名
        "appPackage": "com.dragon.read",  # APP包名
        "appActivity": ".pages.splash.SplashActivity",  # APP启动名
        "skipServerInstallation": "false",
        'unicodeKeyBoard': True,
        'resetKeyBoard': True
    }

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

    logger.info('初始化包名', driver.current_package)
    logger.info('初始化界面控件', driver.current_activity)

    # 超时时间2分钟 每2s检查一次
    explicit_wait = WebDriverWait(driver, 120, poll_frequency=2)


def wait(wait_second=1):
    time.sleep(wait_second)
    logger.info(f'空转{wait_second}秒')


def load_home_page():
    driver.implicitly_wait(60)
    # 显式等待 自定义指定方法 扩展性更好
    # 隐式等待 统一等待多久
    driver.find_element(MobileBy.ID, 'com.dragon.read:id/rz').click()
    logger.info('显示等待--点击我知道了')

    driver.find_element(MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button').click()
    logger.info('显示等待-点击允许')

    driver.find_element(MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button').click()
    logger.info('隐式等待-点击允许')

    driver.find_element(MobileBy.ID, 'com.dragon.read:id/vk').click()
    logger.info('隐式等待-点击跳过')

    logger.info('进入主页')


def bottom_menu_tab2():
    while 1:
        hits = driver.find_elements(MobileBy.ID, 'com.dragon.read:id/j2')
        if len(hits) == 0:
            wait()
            continue

        if hits[0].text.find('分类') > -1:
            return driver.find_elements(MobileBy.ID, 'com.dragon.read:id/j2')
        else:
            wait()


import const


def wait_subtag(d: webdriver.Remote):
    driver.implicitly_wait(0)
    logger.info({
        'current package': driver.current_package, '事件': '加载标签过程中轮询检测网络'})
    xml = etree.XML(driver.page_source.strip('\n\r\t ').split('\n', 1)[1])
    for v in xml.xpath('//android.widget.TextView/@text'):
        if v.find('点击屏幕重试') > -1:
            logger.info('滑动屏幕重试网络')
            swipe_y(0.6, 0.4)
            break
    if driver.current_package.find('dragon') == -1:
        logger.info('app exit')
        raise 'app exit'
    return driver.find_elements(MobileBy.ID, const.xml_subtag_id)


# 点击分类按钮
def find_category_button():
    driver.implicitly_wait(60)
    bottom_menu_tab2()[0].click()
    subtags: List[webdriver.WebElement] = explicit_wait.until(wait_subtag, '找不到二级标签 检查网络或者app卡退')


def get_all_subtags() -> dict:
    global explicit_wait
    category_to_noveltags = dict()
    subtags_all = []
    logger.info('尝试获取顶部标签')
    categories = driver.find_elements(MobileBy.XPATH,
                                      '//android.widget.HorizontalScrollView/android.widget.LinearLayout//android.widget.TextView')
    for category in categories:
        if category.text in ['出版', '男生', '女生']:
            category.click()

            # 存储所有标签
            novel_tag_array = []
            last_tag = ''
            end_confirm = 0
            while 1:
                novel_tags = explicit_wait.until(wait_subtag, '展示小说标签失败')
                # 本页标签全部放到数组中
                # novel_tags = driver.find_elements(MobileBy.ID, 'com.dragon.read:id/ng')
                for novel_tag in novel_tags:
                    print(novel_tag.text)
                    if novel_tag.text not in novel_tag_array:
                        novel_tag_array.append(novel_tag.text)
                swipe_y(0.9, 0.1)
                if novel_tag_array[-1] == last_tag:
                    end_confirm += 1
                    if end_confirm >= 3:
                        logger.error(f'触及底部-{end_confirm}')
                        break
                else:
                    end_confirm = 0
                last_tag = novel_tag_array[-1]

            category_to_noveltags[category.text] = list(set(novel_tag_array))
    return category_to_noveltags


import random


# 两个参数大概是y坐标上的百分比 从下到上滑 0.9-0.1
def swipe_y(y1_pct, y2_pct):
    while 1:
        try:
            size = driver.get_window_size()
            # 定义滑动起始点和终点的坐标
            x1 = size['width'] // 2
            y1 = size['height'] * y1_pct
            x2 = size['width'] // 2
            y2 = size['height'] * y2_pct
            swipe_time = random.randint(1000, 2000)
            logger.info(f"屏幕滑动{x1, y1}-{x2, y2},滑动时间:{swipe_time}")
            driver.swipe(x1, y1, x2, y2, swipe_time)
            return
        except:
            traceback.print_exc()
            wait()


from data import app, fq


def collection_tags():
    # 得到所有模拟器设备
    devices = app.get_all_remote_device_name()
    # 帮的那个模拟器
    bind_device(devices[0])
    load_home_page()
    logger.info('进入主页')
    find_category_button()
    logger.info('点击第二个菜单项')
    category_noveltags = get_all_subtags()

    print(json.dumps(category_noveltags, ensure_ascii=False))
    # app exit
    driver.quit()


def add_tag_to_sqlite():
    extract_sql = fq.extract_dir(__file__) + '/config/novel_tags.json'
    print(extract_sql)
    with open(extract_sql) as conf:
        data = json.loads(conf.read())
        for category, noveltag in data.items():
            for tag in noveltag:
                fq.add_tag(category, tag)


add_tag_to_sqlite()
