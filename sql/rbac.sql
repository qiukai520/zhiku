drop TABLE if exists `users_log`;
create TABLE `users_log`(
`id` int(11) primary key auto_increment,
`user_id` int (11) COMMENT '用户',
`remote_ip` varchar (15) COMMENT '用户',
`content` varchar (128)   COMMENT '操作内容',
`c_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户管理操作记录表';


drop TABLE if exists `user_profile`;
create TABLE `user_profile`(
`id` int(11) primary key auto_increment,
`username` varchar (32) COMMENT '用户' unique ,
`password` varchar (128)   COMMENT '操作内容',
`is_active` tinyint(1)  NOT NULL  DEFAULT 1 COMMENT '状态:0否,1是' ,
`is_superuser` tinyint(1)   NOT NULL   COMMENT '超级用户:0否,1是' ,
`is_deleted` tinyint(1)   NOT NULL  DEFAULT 0 COMMENT '删除状态:0否,1是' ,
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户管理表';




