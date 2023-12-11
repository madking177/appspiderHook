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
from data import app

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


def search_test():
    driver.find_element(MobileBy.ID, 'com.dragon.read:id/nl').click()
    logger.info('点击搜索')

    driver.find_element(MobileBy.ID, 'com.dragon.read:id/mp').send_keys('三体')
    logger.info('搜索小说')

    time.sleep(2)
    driver.find_element(MobileBy.ID, 'com.dragon.read:id/mp').clear()
    logger.info('清空搜索内容')


def novel_category():
    driver.find_element(MobileBy.ID, 'com.dragon.read:id/mm').click()
    driver.find_element(MobileBy.ID, 'com.dragon.read:id/j2').click()

    datas = driver.find_elements(MobileBy.ID, 'com.dragon.read:id/ng')
    for data in datas:
        logger.info(data.text)
    # 点击分类
    datas[0].click()

    #
    driver.find_element(MobileBy.ID, 'com.dragon.read:id/title').click()

    # 新手向导
    driver.find_elements(MobileBy.ID, 'com.dragon.read:id/m9')
    driver.find_elements(MobileBy.ID, 'com.dragon.read:id/mb')

    driver.find_element(MobileBy.ID, 'com.dragon.read:id/yj').click()
    driver.find_element(MobileBy.ID, 'com.dragon.read:id/po').click()

    datas = driver.find_elements(MobileBy.ID, 'com.dragon.read:id/hk')

    for index in range(len(datas)):
        datas[index].click()
        logger.info(datas[index].text)
        driver.find_element(MobileBy.ID, 'com.dragon.read:id/ae').click()
        driver.find_element(MobileBy.ID, 'com.dragon.read:id/po').click()
        driver.find_elements(MobileBy.ID, 'com.dragon.read:id/hk')
    driver.quit()


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
    logger.info({'当前包名': driver.current_package})
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


def find_bottom_tab2():
    driver.implicitly_wait(60)
    bottom_menu_tab2()[0].click()
    subtags: List[webdriver.WebElement] = explicit_wait.until(wait_subtag, '找不到二级标签 检查网络或者app卡退')


def location_novel_tag(location_category, location_tag):
    global explicit_wait
    logger.info('尝试获取顶部标签')
    categories = driver.find_elements(MobileBy.XPATH,
                                      '//android.widget.HorizontalScrollView/android.widget.LinearLayout//android.widget.TextView')
    for category in categories:
        if category.text in [location_category]:
            # 本次分类命中了进行点击
            category.click()
            novel_tag_array = []
            last_tag = ''
            end_confirm = 0
            while 1:
                novel_tags = explicit_wait.until(wait_subtag, '展示小说标签失败')
                # 本页标签全部放到数组中
                for novel_tag in novel_tags:
                    print(novel_tag.text)
                    if novel_tag.text == location_tag:
                        novel_tag.click()
                        logger.warning('找到本次任务标签并进行了点击')
                        return
                    if novel_tag.text not in novel_tag_array:
                        novel_tag_array.append(novel_tag.text)
                swipe_y(0.9, 0.1)
                if novel_tag_array[-1] == last_tag:
                    end_confirm += 1
                    if end_confirm >= 3:
                        logger.error(f'触及底部-{end_confirm}')
                        raise '触及底部都没有命中需要的标签 致命错误'
                else:
                    end_confirm = 0
                last_tag = novel_tag_array[-1]


def extract_text_one(vs) -> str:
    texts = []
    for v in vs:
        texts.append(v.text)
    if len(texts) > 0:
        return texts[0]


def extract_text_array(vs) -> str:
    texts = []
    for v in vs:
        texts.append(v.text)
    if len(texts) > 0:
        return texts[0]


def load_list() -> str:
    tree = etree.XML(driver.page_source.strip('\n\r\t ').split('\n', 1)[1])
    last_title = ''

    for p in tree.xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout'):
        p = etree.tostring(p)
        pp = etree.XML(p)
        title = pp.xpath('//android.widget.TextView[@resource-id="com.dragon.read:id/title"]/@text')
        detail = pp.xpath('//android.widget.TextView[@resource-id="com.dragon.read:id/zl"]/@text')
        grades = pp.xpath('//android.widget.TextView[@resource-id="com.dragon.read:id/a01"]/@text')
        tags = pp.xpath(
            '//android.widget.LinearLayout[@resource-id="com.dragon.read:id/zm"]//android.widget.TextView/@text')

        if len(title) == 0:
            continue
        if len(title) > 0:
            last_title = title[0]

        fq.add_novel(title, detail, grades, tags, location_category, location_tag)

    return last_title


import random


# 两个参数大概是y坐标上的百分比 从小到上滑 0.9-0.1
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
            logger.info('滑动操作异常')
            wait()


def list_swipe_down():
    end_novel_title = ''
    end_confirms = 0
    for index in range(10000):
        # 滑动屏幕 加载列表
        swipe_y(0.9, 0.1)
        end_title = load_list()
        logger.info({'end_title': end_title})
        if end_novel_title == end_title:
            end_confirms += 1
            if end_confirms >= 3:
                logger.info(json.dumps({
                    '翻页': index,
                    '触及底部': end_confirms,
                }, ensure_ascii=False))
                return
        end_novel_title = end_title


from data import fq
import datetime


def app_launch():
    load_home_page()
    find_bottom_tab2()

    location_novel_tag(location_category, location_tag)
    logger.info('进入小说列表页')
    list_swipe_down()


def task_start():
    global location_category, location_tag
    pick_task_sql = f'''select category,tag 
                        from novel_tag 
                        where create_time not like '{datetime.datetime.now().strftime("%Y-%m")}%' 
                        or create_time is null
                        limit 1;'''
    logger.info({'挑选任务': pick_task_sql})
    fq.cursor.execute(pick_task_sql)
    data = fq.cursor.fetchone()
    location_category, location_tag = data[0], data[1]

    logger.info({'分类': location_category, '标签': location_tag})

    # 得到所有模拟器设备
    devices = app.get_all_remote_device_name()
    # 绑定某个设备
    bind_device(devices[0])

    # 重启3次app
    for index in range(3):
        global driver
        try:
            app_launch()
            finish_task = f"update novel_tag set create_time='{datetime.datetime.now()}' " \
                          f"where category='{location_category}' and tag='{location_tag}'"
            logger.warning({'采集完成': finish_task})
            fq.cursor.execute(finish_task)
            fq.conn.commit()
            driver.quit()
            break
        except Exception as e:
            traceback.print_exc()
            logger.error({"error_args": e.args})
    logger.warning('app执行退出')


while 1:
    task_start()
