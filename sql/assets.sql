
drop TABLE if exists `assets`;
create TABLE `assets`(
`nid` int(11)  primary key auto_increment,
`name` varchar (15) NOT NULL COMMENT '名称',
`assets_classify_id` int (11) NOT NULL COMMENT '分类',
`save_number` varchar (32) NOT NULL COMMENT '存档编号',
`save_coordinate_id` int (11) NOT NULL COMMENT '存档坐标',
`quantity` decimal (20,0) NOT NULL COMMENT '数量',
`procurement_time` datetime DEFAULT NULL COMMENT '采购日期',
`procurement_money` decimal (8,2) NOT NULL COMMENT '采购金额',
`procurement_name_id` int(32) NOT NULL COMMENT '采购人',
`invoice` varchar (32) NOT NULL COMMENT '发票',
`user_name_id` int (11) NOT NULL COMMENT '使用人',
`evidence` varchar (32) NOT NULL COMMENT '领取凭证',
`evidence_number` varchar (32) NOT NULL COMMENT '凭据存档编号',
`company_id` int (11) NOT NULL COMMENT '隶属公司',
`project_id` int (11) NOT NULL COMMENT '隶属项目',
`assets_status_id` int (11) NOT NULL COMMENT '资产状态',
`approver_id` int (11) NOT NULL COMMENT '审批人',
`remark` varchar (512) NOT NULL COMMENT '备注',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收入内容表';

drop TABLE if exists `assets_attach`;
create TABLE `assets_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '资产附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='资产附件';


drop TABLE if exists `assetsclassify`;
create TABLE `assetsclassify`(
`id` int (11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '分类'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='分类';

drop TABLE  if exists `save_coordinate`;
create TABLE `save_coordinate`(
`id` int (11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '存档坐标'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='存档坐标';

drop TABLE if exists `procurement_name`;
create TABLE `procurement_name`(
`id` int (11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '采购人'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='采购人';

drop TABLE if exists `user_name`;
create TABLE `user_name`(
`id` int (11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '使用人'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='使用人';

drop TABLE if exists `assets_status`;
create  TABLE `assets_status`(
`id` int (11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '资产状态'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='使用人';