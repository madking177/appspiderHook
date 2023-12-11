# -*- coding: utf-8 -*-

import multiprocessing
import os
import subprocess
import time
import traceback

from loguru import logger


def app(args):
    cmd = f'python ui_driver.py {args}'
    logger.info(cmd)
    os.system(cmd)
    # pass


def firda(args):
    # pass

    cmd2 = f' frida -U  -n com.dragon.read -l ./novel_detail_hook.js --no-pause >> novel_chapter/{args}.txt'
    logger.info(cmd2)
    os.system(cmd2)


from data import fq
import json

if __name__ == '__main__':
    while 1:
        try:
            pick_novel_task = '''select md5,title,detail from novel_info where novel_details_update is null or novel_details_update=0'''
            fq.cursor.execute(pick_novel_task)
            data = fq.cursor.fetchone()
            md5 = data[0]

            logger.info(os.getcwd())
            producer = multiprocessing.Process(target=app, args=(data[0],))
            producer.start()
            logger.info('producer start')
            time.sleep(20)
            logger.info('consumer start')
            consumer = multiprocessing.Process(target=firda, args=(data[0],))

            consumer.start()
            producer.join()
            time.sleep(10)
            fq.cursor.execute(f'''update novel_info set novel_details_update=1 where md5='{md5}' ''')
            fq.conn.commit()
            producer.kill()
            consumer.kill()
            logger.info('producer end')


        except:
            traceback.print_exc()
            try:
                producer.kill()
                consumer.kill()
            except:
                pass
