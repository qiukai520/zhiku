
drop TABLE if exists `revenue`;
create TABLE `revenue`(
`nid` int(11)  primary key auto_increment,
`company_id` varchar (32) NOT NULL COMMENT '公司名称',
`project_id` varchar (32) NOT NULL COMMENT '所在项目',
`income_name` varchar(64) COMMENT '收入名称',
`income_classify_id` varchar(32) NOT NULL COMMENT '收入分类',
`number` varchar(64) COMMENT '存档编号',
`coordinate` varchar(128) COMMENT '存档坐标',
`money` decimal(20,5) NOT NULL COMMENT '收入金额',
`associates_id` varchar(32) COMMENT '关联人',
`approver_id` varchar(32) COMMENT '审批人',
`income_time` datetime DEFAULT NULL COMMENT '收入日期',
`remark` varchar (512) NOT NULL COMMENT '备注',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收入内容表';

drop TABLE if exists `revenue_attach`;
create TABLE `revenue_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '收支附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收支附件';

-- 收入分类
drop TABLE if exists `income_classify`;
create TABLE `income_classify`(
`id` int (11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '收入分类名字'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收入分类';

-- 关联人
drop TABLE if exists `associates`;
create TABLE `associates`(
`id` int (11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '关联人'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='关联人';

-- 审批人
drop TABLE if exists `approver2`;
create TABLE `approver2`(
`id` int (11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '审批人'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='审批人';


-- 支出管理
drop TABLE if exists `disbursement`;
create TABLE `disbursement`(
`nid` int(11)  primary key auto_increment,
`company_id` varchar (32) NOT NULL COMMENT '公司名称',
`project_id` varchar (32) NOT NULL COMMENT '所在项目',
`disbursement_name` varchar(64) COMMENT '支出名称',
`classify_id` varchar(32) NOT NULL COMMENT '支出分类',
`money` decimal(20,5) NOT NULL COMMENT '支出金额',
`associates_id` varchar(32) COMMENT '关联人',
`number` varchar(64) COMMENT '存档编号',
`coordinate` varchar(128) COMMENT '存档坐标',
`approver_id` varchar(32) COMMENT '审批人',
`disbursement_time` datetime DEFAULT NULL COMMENT '支出日期',
`remark` varchar (512) NOT NULL COMMENT '备注',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收入内容表';

drop TABLE if exists `disbur_attach`;
create TABLE `disbur_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '支出附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='支出附件';