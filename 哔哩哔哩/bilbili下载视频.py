import requests
import re
import time
import pprint # 导入格式化输出模块
import json
import subprocess # 导入进程模块
import os


# 发送请求
# https://www.bilibili.com/video/BV1U541137Eb?spm_id_from=333.337.search-card.all.click

url = input('请输入B站视频链接:')
headers = {
'referer': 'https://www.bilibili.com/a', # 防盗链 告诉服务器 我们请求的url网址是从哪里跳转过来的
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
response = requests.get(url=url, headers=headers)
html = response.text
# print(response)  # <response[200]>响应对象


# 解析数据
time.sleep(2)
# <h1 id="video-title" title="(.*?)" class="video-title"><a target="_blank" class="activity">活动作品</a><span class="tit">漂亮的穿旗袍美女剪超短发</span></h1>
# 视频标题
# title = re.findall('<h1 title="(.*?)" class="video-title tit">.*?</h1>', html, re.S)[0]
# title = re.sub(r'[\/:-?*&"<>| 》《]', '', title)
title = '魔女之旅素材库'
html_data = re.findall('<script>window.__playinfo__=(.*?)</script>', html)[0]
# print(title)
# print(html_data)
# 将html转化成字典
json_data = json.loads(html_data)
# print(json_data)
# pprint.pprint(json_data)
# print(type(json_data))

# 字典取值
audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
video_url = json_data['data']['dash']['video'][0]['baseUrl']
# print(audio_url)
audio_content = requests.get(url=audio_url, headers=headers).content
video_content = requests.get(url=video_url, headers=headers).content
with open(title + '.mp3', 'wb') as f:
    f.write(audio_content)
with open(title + '.mp4', 'wb') as f:
    f.write(video_content)
print(title, '下载完成')
title1 = title.replace(' ', '')
print(title)
cmd = f"ffmpeg -i {title}.mp4 -i {title}.mp3 -c:v copy -c:a aac -strict experimental {title}output.mp4"
# cmd = f'ffmpeg -i {title}.mp4 -i {title}.mp3 {title}output.mp4'
subprocess.run(cmd, shell=True)
os.remove(f'{title}.mp4')
os.remove(f'{title}.mp3')
print(title, '视频合成完成')