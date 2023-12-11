# -*- coding: utf-8 -*-
# 1.导入appium
import json
import random
import time
import traceback
from lxml import etree
import re
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.appiumby import AppiumBy as MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from typing import List
from loguru import logger
import subprocess


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
            time.sleep(1)


def click(x, y):
    logger.info({
        'x': x,
        'y': y
    })
    TouchAction(driver).tap(x=x, y=y).perform()


def search_and_wait(hit_text):
    count = 0
    while driver.page_source.find(hit_text) == -1:
        count += 1
        time.sleep(1)
        logger.info(count)
        if count > 10:
            return


def find_and_click(hit_text):
    for v in driver.find_elements(MobileBy.XPATH, '//android.widget.Button'):
        v1 = v.get_attribute('text')
        v2 = v.get_attribute('content-desc')
        if ''.join(re.findall(r'[\u4e00-\u9fff]+', v1 + v2)).find(hit_text) > -1:
            v.click()
            return
    for v in driver.find_elements(MobileBy.XPATH, '//android.view.View'):
        v1 = v.get_attribute('text')
        v2 = v.get_attribute('content-desc')
        if ''.join(re.findall(r'[\u4e00-\u9fff]+', v1 + v2)).find(hit_text) > -1:
            v.click()
            return


# device = '127.0.0.1:16384'
device = '4755bad00204'
driver: webdriver.webdriver.WebDriver
# subprocess.run(f'adb connect {device}', capture_output=True)
desired_caps = {
    'automationName': 'Appium',  # add this line
    "platformName": "Android",  # 系统名称
    "platformVersion": "9",  # 系统版本
    # "deviceName": "emulator-5554",  # 设备名称
    # "udid": "emulator-5554",  # 设备名称
    "deviceName": device,  # 设备名称
    "udid": device,  # 设备名称
    "appPackage": "com.taobao.idlefish",  # APP包名
    "appActivity": "com.taobao.fleamarket.home.activity.InitActivity",  # APP启动名
    "skipServerInstallation": "false",
    'unicodeKeyBoard': True,
    'resetKeyBoard': True
}
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

logger.info('初始化包名', driver.current_package)
logger.info('初始化界面控件', driver.current_activity)

driver.find_element(MobileBy.ID, 'com.taobao.idlefish:id/right_btn').click()
driver.implicitly_wait(60)
login_check = True
while login_check:
    text_all = []
    for text in driver.find_elements(MobileBy.XPATH, '//android.widget.TextView'):
        text_all.append(text.text)
        if text.text in ['欢迎来到闲鱼', '您已阅读并同意《闲鱼社区用户服务协议》 《隐私权政策》', '其他登录方式']:
            login_check = False
            break
TouchAction(driver).tap(x=115, y=205).perform()

logger.info('进入主页')

driver.find_element(MobileBy.ID, 'com.taobao.idlefish:id/tv_search').click()
driver.find_element(MobileBy.CLASS_NAME, 'android.widget.EditText').send_keys('iphone')
driver.find_element(MobileBy.XPATH, '//android.view.View[@content-desc="搜索"]').click()
time.sleep(2)
driver.find_element(MobileBy.XPATH, '//android.widget.Button[@content-desc="最​新​发​布​"]').click()
time.sleep(3)
for i in range(5):
    res = driver.find_elements(MobileBy.XPATH, '//android.widget.ImageView')
    for v in res:
        print(v.get_attribute("content-desc"))
        tmpv = v.get_attribute("content-desc")
        if tmpv is None or len(tmpv) < 20:
            continue
        v.click()
        time.sleep(1)
        logger.info('点击进入详情页')
        text = []
        for v in driver.find_elements(MobileBy.XPATH, '//android.view.View'):
            text.append(v.get_attribute('content-desc'))

        logger.info(text)
        driver.save_screenshot(f'{time.time()}.png')
        swipe_y(0.8, 0.2)
        driver.save_screenshot(f'{time.time()}.png')

        driver.find_elements(MobileBy.CLASS_NAME, "android.view.View")[0].click()
        logger.info('返回')
        # driver.find_element(MobileBy.XPATH,'//android.view.View[@content-desc="返回"]').click()
        time.sleep(100)
        driver.find_elements(MobileBy.CLASS_NAME, "android.view.View")[0].click()
        driver.find_element(MobileBy.XPATH, '//android.view.View[@content-desc="返回"]').click()

    swipe_y(0.6, 0.2)
    # driver.save_screenshot(f'{time.time()}.png')
