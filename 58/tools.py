# -*- coding: utf-8 -*-
import json
import traceback
from selenium.webdriver.common import by

import time
import string
import zipfile
from selenium import webdriver

driver = None
from loguru import logger
import requests


# 得到客户端
def get_chrome_client() -> webdriver.Chrome:
    global driver

    while 1:
        if driver is not None:
            try:
                driver.close()
                driver.quit()
            except:
                traceback.print_exc()
        # logger.info({'index': proxy_index, 'ip': cuts})
        chrome_options = webdriver.ChromeOptions()
        #         代理插件
        if True:
            r = requests.get('')

            remaining_ip_count = requests.get('')

            logger.info({'大麦代理ip': r.text, 'ip剩余量': remaining_ip_count.text})

            cuts = r.text.strip('\n\r\t ').split(':')

            ip, port = cuts[0], cuts[1]

            proxy_auth_plugin_path = create_proxy_auth_extension(
                proxy_host=ip,
                proxy_port=port,
                proxy_username='',
                proxy_password='')
            chrome_options.add_extension(proxy_auth_plugin_path)  # 添加proxy插件

        # chrome_options.add_argument("--start-maximized")  # 窗口最大化运行
        chrome_options.add_argument("--blink-settings=imagesEnabled=true")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--incognito')
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        # driver.execute_script('''
        #     Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
        #     ''')
        driver.implicitly_wait(60)

        return driver


# 创建插件
def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http',
                                plugin_path=None):
    if plugin_path is None:
        plugin_path = r'./{}_{}_qgnet_proxyauth_plugin.zip'.format(proxy_username, proxy_password)
    manifest_json = """
       {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
        }
        """
    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["localhost"]
            }
          };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_path


def wait(sec=1):
    logger.info(f'等待 {sec} 秒')
    time.sleep(sec)


class myResp():
    def __init__(self, text):
        self.text = text


index = 0


def request_get(url) -> myResp:
    time.sleep(3)
    global index
    time.sleep(1)
    index += 1
    logger.info({'url': url})
    # 每次访问前做一次验证码检查
    global driver
    while 1:
        driver.get(url)
        if driver.page_source.find('antibot/verifycode') > -1 or driver.page_source.find(
                '访问过于频繁，请登录后继续访问'):
            logger.error({'遭遇验证码': index})
            time.sleep(3)
            driver = get_chrome_client()
        else:
            break
    # 禁用了js
    return myResp(driver.page_source)
