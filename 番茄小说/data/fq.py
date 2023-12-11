import datetime
import json
import hashlib
import re

from .db import cursor, conn
from loguru import logger


def add_novel(title: list, details: list, grades: list, tags: list, location_category: str, location_tag: str):
    title = json.dumps(title, ensure_ascii=False).replace("'", "")
    values = []
    values.append(hashlib.md5(title.encode()).hexdigest())
    values.append(title)
    values.append(json.dumps(details, ensure_ascii=False).replace("'", ""))
    values.append(json.dumps(grades, ensure_ascii=False).replace("'", ""))
    values.append(json.dumps(tags, ensure_ascii=False).replace("'", ""))

    logger.info(values)
    insert_sql = (
        f"replace into novel_info('md5','title','detail','grades','tags','create_time','update_time','category','tag') "
        f"values('{values[0]}','{values[1]}','{values[2]}','{values[3]}','{values[4]}',"
        f"'{datetime.datetime.now()}','{datetime.datetime.now()}','{location_category}','{location_tag}')")
    # logger.info(insert_sql)
    cursor.execute(insert_sql)
    conn.commit()


def add_tag(category, novel_tag):
    insert_sql = (f"replace into novel_tag(category,tag) values ('{category}','{novel_tag}')")
    logger.info(insert_sql)
    cursor.execute(insert_sql)
    conn.commit()


def extract_dir(file_path: str):
    directory = re.findall('.*/', file_path.replace('\\', '/'))[0]
    return directory
