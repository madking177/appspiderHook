CREATE TABLE novel_tag
(
    category text,-- ����  ���� ���� Ů��
    tag      text, --��ǩ����
    create_time --����ʱ��
);

create table novel_info
(
    md5         text primary key, --title��md5��������
    title       text,-- С˵����
    detail      text,-- С˵ժҪ ���
    grades      text,             -- С˵����
    tags        text,             -- С˵��ǩ
    create_time text,             --����ʱ��
    update_time text              --�޸�ʱ��
)