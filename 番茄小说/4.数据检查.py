import os
import re
from data import db


def check_novel_chapter_data():
    target_dir = re.findall('.*/', __file__.replace('\\', '/'))[0] + 'novel_chapter/'
    for filename in os.listdir(target_dir):

        fullpath = target_dir + filename
        hashcode = filename.split('.txt')[0]
        datasize = os.path.getsize(fullpath)

        if datasize < 1024:
            print(hashcode, 'data error')
            db.cursor.execute(f"update novel_info set novel_details_update=0 where md5='{hashcode}' ")
            db.conn.commit()
            os.remove(fullpath)


check_novel_chapter_data()
