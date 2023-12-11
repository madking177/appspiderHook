import hashlib
import json
import pprint
import sys
from loguru import logger
import frida

d = frida.get_remote_device()
session = d.attach('com.dragon.read')


def on_msg(msg, data):
    print(msg, data)


js = open('js/gorgon.js', encoding='utf8').read()

script = session.create_script(js)

script.on('message', on_msg)
script.load()


def get_md5(v):
    return hashlib.md5(v.encode('utf8')).hexdigest()


item = '7185749769396945440'

start_url = f'https://reading.snssdk.com/reading/reader/full/v/?item_id={item}&iid=3485926985040344&device_id=4277575347096887&ac=wifi&mac_address=00%3ADB%3AC7%3AE8%3A7E%3A26&channel=wandoujia&aid=1967&app_name=novelapp&version_code=300&version_name=3.0.0.32&device_platform=android&ssmix=a&device_type=GM1900&device_brand=OnePlus&language=zh&os_api=28&os_version=9&uuid=010306022462377&openudid=9d88af7749ae10ec&manifest_version_code=300&resolution=1920*1080&dpi=280&update_version_code=30032&_rticket=1693110872439&gender=0&comment_tag_c=3&vip_state=0&imei=010306022462377&category_style=1&cdid=94d751c6-2fc3-4ca1-8b73-44d28c96d1ea'
import re

url = re.findall(r'\?.*#?', start_url)[0].strip('\r\n\t?')
get_md5(url)

cookie = 'store-region=cn-jl; store-region-src=did; install_id=3485926985040344; ttreq=1$a393e74bab0d63645cded553eb956801203e489d; odin_tt=2e8429f024a8a6557821611b11ad5aa757073175449b1f9f6223ecb8750f8f18808e9d94bc3e541422d390c9d84cc8b4f591a3862ec3799b4604d9e78ba82c5d98890f7fe176ba799298b72d5b01fd74'

time = 1693110872

pprint.pprint({'url': url, 'cookie': cookie, })

v1 = -1
v2 = time
v3 = f"{get_md5(url)}{'0' * 32}{get_md5(cookie)}{'0' * 32}"

pprint.pprint({
    'v1': v1,
    'v2': v2,
    'v3': v3,
})
int_array = script.exports.gorgon_str128(v1, v2, v3)
token_gorgon = script.exports.gorgon_string(int_array)

headers = {
    'accept-encoding': 'gzip',
    'accept': 'application/json; charset=utf-8',
    'x-xs-from-web': '0',
    'x-ss-queries': 'dGMFEAAAKswmfUy%2BRVr2QOSnB6hGkj%2BN5AHOhQUpdgn2QF9150oAJOXARo3sbQjRL7BOGYkDLX9j3PYAo%2BM6%2FiJaHiclYTsIO8dWvV9mZWUadFyJoIj0dIGPr7kzRoNJnPk806ZOn7yPLiEs6hY7a6laUQkwHljHcZ0QJ25jvfUTfT%2Fh8SMk3MrP7GnnJJeZz5RHdbqLGdXl2hMHxRKyEuR7nhATA3LN01L4JoXEnMza4B8TcIVMnYMkeplwm5kEQ%2B1ELZjkJ3YxwL3Pcy%2FefwGBumQIs3mb51j9htBQED7mWJ4ajCw%3D',
    'x-ss-req-ticket': '1693110872444',
    'x-reading-request': '1693110872444-1531567682',
    'gender': '0',
    'sdk-version': '1',
    'user-agent': 'ttnet okhttp/3.10.0.2',
    'cookie': 'store-region=cn-jl; store-region-src=did; install_id=3485926985040344; ttreq=1$a393e74bab0d63645cded553eb956801203e489d; odin_tt=2e8429f024a8a6557821611b11ad5aa757073175449b1f9f6223ecb8750f8f18808e9d94bc3e541422d390c9d84cc8b4f591a3862ec3799b4604d9e78ba82c5d98890f7fe176ba799298b72d5b01fd74',
    'x-khronos': f'{time}',
    'x-gorgon': f'{token_gorgon}',
}

import requests

r = requests.get(url=start_url, headers=headers)

print(r.status_code)
print(r.text)
# 同步一下进度
# 破解环境 雷电模拟器，charles，frida，jadx ，gda
# 最新六神加密算法  很难破解，两天无进展 换低版本app
# api降为四神加密算法token 通过反编译代码已经分析出来出加密方式 最底层得加密算法封装在so文件 所以通过hook方式获得 so加密入参 分别为-1，时间，url+cookie得摘要串
# firda-rpc得方式可以获得gorgon-token
#
# 可以通过章节id拿到小说，小说内容加密 搞定还需要一步反编译 估计还得几天
#
# 当接口搞定后 执行计划大概是通过app得第二个tab标签拿到所有一级分类，二级分类信息，逐步下拉请求
#
# 最终部署 ：模拟器+frida-hook+charles+python+nodejs
#
#
# 起点app目前在雷电模拟器会卡退，还没开始分析，换模拟器，手机等方式后续推进

