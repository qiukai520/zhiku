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


DROP TABLE IF EXISTS `user_profile`;
CREATE TABLE `user_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


drop TABLE if exists `user_role`;
create TABLE `user_role`(
`id` int(11) primary key auto_increment,
`user_id` int (16) COMMENT '用户',
`role_id` varchar (128)   COMMENT '角色'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户角色关系表';

