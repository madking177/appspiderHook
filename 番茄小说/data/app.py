# -*- coding: utf-8 -*-

import subprocess
from loguru import logger
import platform


# 得到所有模拟器得设备名称
def get_all_remote_device_name():
    if platform.system().lower().find('windows') == -1:
        logger.error('禁止在非windows系统运行本程序')
    output_rows = str(subprocess.run('adb devices'.split(' '), capture_output=True).stdout, 'utf8').split('\r\n')
    device_names = []
    for row in output_rows:
        if row != '' and row.startswith('emulator'):
            device_names.append(row.split('\t')[0])
    logger.info({'得到设备列表': device_names})

    return device_names
