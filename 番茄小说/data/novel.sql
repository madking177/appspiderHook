CREATE TABLE novel_tag
(
    category text,-- 分类  出版 男生 女生
    tag      text, --标签名称
    create_time --创建时间
);

create table novel_info
(
    md5         text primary key, --title得md5码做主键
    title       text,-- 小说标题
    detail      text,-- 小说摘要 简介
    grades      text,             -- 小说评分
    tags        text,             -- 小说标签
    create_time text,             --创建时间
    update_time text              --修改时间
)