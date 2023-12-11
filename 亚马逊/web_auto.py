# -*- coding: utf-8 -*-
import json
import traceback
from loguru import logger
from selenium.webdriver.common import by

import time
import string
import zipfile
from selenium import webdriver

driver = None


# 定位日本 虽然没有调用 但是必须保留代码段未来使用
def locate_japan(driver):
    driver.find_element(by.By.XPATH, "//span[@id='glow-ingress-line2']").click()
    wait(1)
    # 填写邮政编码
    driver.find_element(by.By.XPATH, "//input[@id='GLUXZipUpdateInput_0']").send_keys('190')
    driver.find_element(by.By.XPATH, "//input[@id='GLUXZipUpdateInput_1']").send_keys('0015')
    wait(1)
    driver.find_element(by.By.XPATH, '//input[@aria-labelledby="GLUXZipUpdate-announce"]').click()
    wait(1)
    logger.info({'事件': '保存位置'})

    driver.refresh()
    # driver.find_element('//span[@id="GLUXConfirmClose-announce"]').click()
    # data = driver.find_element(by.By.XPATH, '//span[@id="glow-ingress-line2"]')
    # if data.text.find('立川') == -1:
    #     logger.error('定位异常 退出')
    #     exit()
    # logger.info(f'输入 邮编190 0015 进行定位 位置:{data.text}')


def get_chrome_client() -> webdriver.Chrome:
    global proxy_index, black_index, driver

    while 1:
        try:
            if driver is not None:
                try:
                    driver.close()
                    driver.quit()

                except:
                    traceback.print_exc()
            proxy_index = int(time.time() % len(ips))
            cuts = ips[proxy_index].replace('http://', '').split(':')
            uname, upass, ip, port = cuts[0], cuts[1], cuts[2], cuts[3]
            proxyHost = ip  # 代理IP地址
            proxyPort = port  # 代理IP端口号
            authKey = uname  # 代理IP的AuthKey
            password = upass  # 代理IP的AuthPwd

            logger.info({'index': ips[proxy_index]})
            proxy_auth_plugin_path = create_proxy_auth_extension(
                proxy_host=proxyHost,
                proxy_port=proxyPort,
                proxy_username=authKey,
                proxy_password=password)

            # logger.info({'index': proxy_index, 'ip': cuts})
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--start-maximized")  # 窗口最大化运行
            chrome_options.add_extension(proxy_auth_plugin_path)  # 添加proxy插件
            chrome_options.add_argument("--blink-settings=imagesEnabled=false")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")

            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script('''
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
            ''')
            driver.implicitly_wait(60)

            try:
                driver.get('https://www.amazon.co.jp/')
            except:
                traceback.print_exc()
                continue
            if driver.page_source.find('この画像に見える文字を入力してください:') > -1 or driver.page_source.find(
                    '无法访问此网站') > -1:
                logger.error('遇到验证码 重启浏览器 或者断网重启浏览器')
                continue
            driver.implicitly_wait(60)
            driver.get('https://myip.ipip.net/')
            time.sleep(1)
            driver.get('https://www.amazon.co.jp/')
            driver.find_element(by.By.XPATH, '//a[@id="icp-nav-flyout"]').click()
            els = driver.find_elements(by.By.XPATH,
                                       '//div[@class="a-row a-spacing-mini"]//div[@data-a-input-name="lop"]')
            for e in els:
                if e.text.find('日本') > -1:
                    e.click()
            driver.find_element(by.By.XPATH, '//span[@class="a-button-inner"]/input[@class="a-button-input"]').click()
            logger.info('切换日文')
            time.sleep(1.5)
            locate_japan(driver)
            break
        except:
            traceback.print_exc()

    return driver


ips = []
with open('config.json') as f:
    datas = json.load(f)['proxies']
    for data in datas:
        ip = data.replace('http://', '').replace('@', ':')
        print(ip)

        ips.append(ip)


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


proxy_index = 0
