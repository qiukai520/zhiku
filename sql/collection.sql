
drop TABLE if exists `coll_record`;
create TABLE `coll_record`(
`nid` int(11)  primary key auto_increment,
`tid_id` int(11) default 0 COMMENT '工单关联',
`origin` int(11) default 0 COMMENT '原数据',
`title` varchar(512) COMMENT '标题',
`summary` varchar(512) COMMENT '总结',
`remark` varchar(512) COMMENT '备注',
`tag` varchar(128) COMMENT '标签',
`relate_tag` varchar(128) COMMENT '关联标签',
`industry` varchar(512) COMMENT '关联行业',
`relate_title` varchar(128) COMMENT '关联标题',
`recorder_id`  int(11) NOT NUll DEFAULT 0 COMMENT'收录人',
`contributor_id`  int(11) NOT NUll DEFAULT 0 COMMENT'贡献人',
`type_id`  int(11) NOT NUll DEFAULT 0 COMMENT'类型',
`favor`  int(11) NOT NUll DEFAULT 0 COMMENT'点赞数',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收录内容表';


drop TABLE if exists `coll_attach`;
create TABLE `coll_attach`(
`nid` int(11) primary key auto_increment,
`tsid_id`  int(11) NOT NULL COMMENT '收录内容',
`attachment` varchar(512) COMMENT '附件',
`name` varchar(128) COMMENT '附件名称',
`description` varchar(512) COMMENT '附件描述',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收录内容附件表';


drop TABLE if exists `coll_favor`;
create TABLE `coll_favor`(
`nid` int(11) primary key auto_increment,
`tsid_id`  int(11) NOT NULL COMMENT '收录内容',
`uid_id`  int(11) NOT NULL COMMENT '点赞人',
`status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '状态:0取消,1有用',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收录点赞表';
alter table coll_favor  ADD UNIQUE KEY `cf_id`(`uid_id`,`tsid_id`) USING BTREE;
