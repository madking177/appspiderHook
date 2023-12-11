# -*- coding: utf-8 -*-
from loguru import logger
import sqlite3,re

db_file = re.findall('.*/', __file__.replace('\\', '/'))[0] + './z_fanqie_novel.db'
# 连接到SQLite数据库，如果数据库不存在则会自动创建
conn = sqlite3.connect(db_file)
logger.info(f'加载数据库文件 {db_file}')
cursor = conn.cursor()
# 创建一个游标对象
cursor.execute('select name from sqlite_master where type="table"')

cursor_print_sql = conn.cursor()
for table in cursor.fetchall():
    table = table[0]
    cursor_print_sql.execute(f'''SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';''')
    sql = cursor_print_sql.fetchone()
    logger.info({'表名': f'{table}', '建表语句': sql})
cursor_print_sql.close()
logger.info('打印数据库信息')

cursor.execute('select * from novel_info limit 5')
for row in cursor.fetchall():
    logger.info(row)
