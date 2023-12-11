# -*- coding: utf-8 -*-
import datetime

novels = [
    "中国名著",
    "经济管理",
    "影视小说",
    "哲学宗教",
    "政治军事",
    "经典国学",
    "个人成长",
    "亲子家教",
    "时尚美妆",
    "诗歌散文",
]

for novel in novels:
    print(ord(novel[0]))

t = datetime.datetime.now().strftime("%Y-%m")

print(t)
