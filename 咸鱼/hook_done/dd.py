# <<<<<<< HEAD
# from PIL import Image
#
# # 打开图片
# image1 = Image.open('1696843956.882459.png')
# image2 = Image.open('1696843958.5451064.png')
#
# # 获取两个图片的尺寸
# width1, height1 = image1.size
# width2, height2 = image2.size
#
# # 新的图片的尺寸应该是两个图片的尺寸之和
# new_width = width1 + width2
# new_height = max(height1, height2)
#
# # 创建一个新的图片对象
# new_image = Image.new('RGB', (new_width, new_height))
#
# # 在新的图片上拼接两个图片
# new_image.paste(image1, (0, 0))
# new_image.paste(image2, (width1, 0))
#
# # 保存新的图片
# new_image.save('merged_image.png')
# =======
import json

import requests


def send_dingding(desc, publish_time, ts, item_id, img_url, price):
    for dd_bot in [
        'https://oapi.dingtalk.com/robot/send?access_token=7a3bcac2c3b0dc3c50ac598c8a4c267363a5acade8257b7f933827c981c27bf9', ]:
        r = requests.post(
            dd_bot,
            headers={
                'Content-Type': 'application/json',
            },
            data=json.dumps({
                "msgtype": "actionCard",
                "actionCard": {
                    "title": "fish-demo",
                    "text": f"![screenshot]({img_url}) \n\n ##### 1.描述:{desc}\n\n\n\n##### 2.时间:{publish_time}\n\n##### 3.发布状况:{ts}\n\n### 4.价格:{price}",
                    "btnOrientation": "0",
                    "btns": [
                        {
                            "title": "跳转咸鱼-点击直接进入app",
                            "actionURL": f"fleamarket://item?id={item_id}"
                        },
                    ]
                }
            }))
        print(r.text)
