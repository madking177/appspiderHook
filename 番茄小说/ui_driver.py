# -*- coding: utf-8 -*-

# 1.导入appium
import json
import multiprocessing
import os
import sys
import time
import traceback
from lxml import etree

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from typing import List
from loguru import logger
from data import app
import re

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
            swipe_time = random.randint(700, 1500)
            logger.info(f"屏幕y轴滑动{x1, y1}-{x2, y2},滑动时间:{swipe_time}")
            driver.swipe(x1, y1, x2, y2, swipe_time)
            return
        except:
            traceback.print_exc()
            logger.info('滑动操作异常')
            wait()


def swipe_x(x1_pct, x2_pct):
    while 1:
        try:
            size = driver.get_window_size()
            # 定义滑动起始点和终点的坐标
            x1 = size['width'] * x1_pct
            y1 = size['height'] // 2
            x2 = size['width'] * x2_pct
            y2 = size['height'] // 2
            swipe_time = random.randint(600, 1000)
            logger.info(f"屏幕x轴滑动{x1, y1}-{x2, y2},滑动时间:{swipe_time}")
            driver.swipe(x1, y1, x2, y2, swipe_time)
            return
        except:
            traceback.print_exc()
            logger.info('滑动操作异常')
            wait()


from data import fq
import datetime


def load_chapter(data, title, abstract):
    logger.info({'任务': data})
    load_home_page()

    logger.info('点击搜索框')
    driver.find_element(MobileBy.ID, "com.dragon.read:id/nl").click()
    logger.info(f'输入 {title}')
    driver.find_element(MobileBy.ID, "com.dragon.read:id/mp").send_keys(title)
    logger.info('点击搜索')
    driver.find_element(MobileBy.ID, "com.dragon.read:id/mo").click()

    novel_list_by_search = driver.find_elements(MobileBy.ID, "com.dragon.read:id/ht")
    find_novel=False
    # 通过搜索列表找到具体的小说
    for novel_title in novel_list_by_search:
        if novel_title.text.strip(' ') == title.strip(' '):
            logger.info({'title命中了': novel_title.text})
            novel_title.click()
            logger.info('进入了小说章节页面')
            find_novel=True
            break
    if find_novel:
        logger.info('开始获取小说详情')
        for i in range(120):
            if driver.page_source.find('点击中间显示菜单') > -1:
                break
            else:
                wait()

        logger.info('点击向导页面')
        driver.find_element(MobileBy.ID, 'com.dragon.read:id/ag4').click()
        driver.find_element(MobileBy.ID, 'com.dragon.read:id/mc').click()

        if driver.page_source.find('上一章') > -1 and driver.page_source.find('下一章') > -1:
            logger.info('无序点击 进度条已经展示')
        else:
            logger.info('需要点击 进度条没有展示 执行点击事件')
            TouchAction(driver).tap(driver.get_window_size()['width'] // 2,
                                    driver.get_window_size()['height'] // 2).perform()

        # driver.find_element(MobileBy.ID, 'com.dragon.read:id/a8x').click()
        logger.info('点击左侧目录')
        driver.find_element(MobileBy.ID, 'com.dragon.read:id/po').click()

        driver.find_element(MobileBy.ID, 'com.dragon.read:id/aai')
        logger.info('小说左侧的章节目录已经出现')


        total=driver.find_element(MobileBy.ID,'com.dragon.read:id/aal')

        total=int(''.join(re.findall('[0-9]{1,}', total.text)))

        logger.info({'总章节数':total})


        first_chapter = ''
        while 1:
            swipe_y(0.3,0.9)
            ls = []
            for v in driver.find_elements(MobileBy.ID, 'com.dragon.read:id/hk'):
                ls.append(v.text)
            if first_chapter == ls[0]:
                logger.info('结束循环')
                break
            else:
                first_chapter = ls[0]

        logger.info({'小说第一章': first_chapter})

        driver.find_elements(MobileBy.ID, 'com.dragon.read:id/hk')[0].click()

        logger.info({'事件':'点击第一章 复位'})
        # logger.info('屏幕横向滑动 收起章节菜单')
        # swipe_x(0.9, 0.1)

        logger.info('开始点击下一章')
        wait()

        if driver.page_source.find('上一章') > -1 and driver.page_source.find('下一章') > -1:
            logger.info('无序点击 进度条已经展示')
        else:
            logger.info('需要点击 进度条没有展示 执行点击事件')
            TouchAction(driver).tap(x=driver.get_window_size()['width'] // 2,
                                    y=driver.get_window_size()['height'] // 2).perform()

        # for i in range(0, total):
        #     logger.info({'index':total-i})
        #     点击上一章进行位置还原
            # driver.find_element(MobileBy.ID, 'com.dragon.read:id/ag7').click()

        for i in range(0, total):
            logger.info({'当前点击次数': i, '总章节': total})
            driver.find_element(MobileBy.ID, 'com.dragon.read:id/ag8').click()
            wait(1)

        logger.info('小说抓取完毕 继续下一步小说抓取')

    driver.quit()

import subprocess

import signal




def app_start():
    pick_novel_task = f'''select md5,title,detail from novel_info where md5='{sys.argv[1]}' '''
    fq.cursor.execute(pick_novel_task)
    vv = fq.cursor.fetchone()
    load_chapter(vv[0], json.loads(vv[1])[0], json.loads(vv[2])[0], )


# 得到所有模拟器设备
devices = app.get_all_remote_device_name()
# 绑定某个设备
bind_device(devices[-1])
app_start()
logger.warning('app执行退出')

