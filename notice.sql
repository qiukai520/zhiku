
drop TABLE  if  exists `notice`;
create table `notice`(
`nid` int(11) primary key auto_increment,
`notice_status` tinyint(1) NOT NULL COMMENT '阅读状态',
`notice_title` varchar (64)  COMMENT '标题',
`notice_body` varchar (128)   COMMENT '内容',
`notice_url` varchar (64) COMMENT'父链接' ,
`notice_type` varchar (64) COMMENT'通知类型' ,
`user_id`int(11) NOT NULL COMMENT '用户',
`notice_time`  datetime  DEFAULT NUll  COMMENT '通知时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通知';