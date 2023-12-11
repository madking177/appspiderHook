# -*- coding: utf-8 -*-
def format_curl_command(curl_command):
    # 分割命令行为单独的部分
    parts = curl_command.split(' ')

    formatted_command = []
    for part in parts:
        if part.startswith('-H'):
            # 新的HTTP头开始了，换行并添加HTTP头
            formatted_command.append("\\\n" + part)
        else:
            # 否则，继续在同一行添加命令部分
            formatted_command.append(part)

    return ' '.join(formatted_command)


with open('获取详情的请求.txt') as f:
    for row in f:
        print(format_curl_command(row))
