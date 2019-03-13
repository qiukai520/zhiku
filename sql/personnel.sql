
drop TABLE if exists `s_project`;
create TABLE `s_project`(
`id`int(11) primary key auto_increment,
`name` varchar(64) NOT NULL COMMENT '项目名'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='项目名';

drop TABLE if exists `article`;
create TABLE `article`(
`id`int(11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '用品'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用品';

drop TABLE if exists `reasons_people`;
create TABLE `reasons_people`(
`id`int (11) primary key auto_increment,
`name` varchar (64) NOT NULL COMMENT '工作交接人'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='工作交接人';

drop TABLE if exists `reasons_cause`;
create TABLE `reasons_cause`(
`id` int (11) primary key auto_increment,
`cause` varchar (64) NOT NULL COMMENT '原因'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='原因';

drop table if exists `performanceyg`;
create table `performanceyg`(
`nid` int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT'员工',
`select_project_id_id` int(11) NOT NULL COMMENT '选择项目',
`content` varchar(512) NOT NULL COMMENT '内容明细',
`effective_time` datetime  DEFAULT NUll  COMMENT '生效日期',
`create_time`  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '生效时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间',
`operator_id` varchar (11) COMMENT '操作人'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='增加就职表现';

drop TABLE if exists `Perforygmance_Attach`;
create TABLE `Perforygmance_Attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '就职附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='就职附件';

drop TABLE if exists `labor_contract`;
create TABLE `labor_contract`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '员工',
`remark` varchar(512) NOT NULL COMMENT '备注',
`create_time` datetime DEFAULT NULL COMMENT '开始时间',
`end_time` datetime DEFAULT NULL COMMENT '结束时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='劳动合同';

drop TABLE if exists `labor_contract_attach`;
create TABLE `labor_contract_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '劳动合同附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='劳动合同附件';

drop table if exists `reasonsleave`;
create table `reasonsleave`(
`nid`int (11) NOT NUll primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT'员工',
`reasons_cause` int(11) NOT NULL COMMENT '原因',
`reasons` varchar (512) NOT NULL COMMENT '离职原因',
`reasons_time` datetime DEFAULT NULL COMMENT '工资计算截止日期',
`reasons_bool1` tinyint(1) default 0 COMMENT '停用账号选择状态：0=否，1=是',
`reasons_bool2` tinyint(1) default 0 COMMENT '停买社保选择状态',
-- `reasons_id_id` int(11) NOT NULL COMMENT '用品',
`reasons_people_id` int(11) NOT NULL COMMENT '工作交接人',
`reasons_time1` datetime DEFAULT NULL COMMENT '离岗日期'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='离岗原因';

-- 离职附件
drop TABLE if exists `reasons_attach`;
create TABLE `reasons_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '劳动合同附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='离职附件';

drop table if exists  `social_security`;
create table `social_security`(
`nid`int (11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '员工',
`s_id` varchar (80) NOT NULL COMMENT '社保卡号',
`s_money` decimal (20,10) NOT NULL COMMENT '购买金额',
`s_time` datetime DEFAULT NULL COMMENT '起始时间',
`s_remark` varchar (512) NOT NULL COMMENT '备注'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='社保管理';

drop table if exists `social_attach`;
create table `social_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '社保附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='社保附件';


drop table if exists `supplies`;
create table `supplies`(
`nid` int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '员工',
`supplies_id_id` int(11) NOT NULL COMMENT '用品',
`supplies_time` datetime DEFAULT NULL COMMENT '领用日',
`supplies_remark` varchar (512) NOT NULL COMMENT '备注'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用品领用';

drop table if exists `supplies_attach`;
create table `supplies_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '用品领用附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用品领用附件';


drop table if exists `supplies_return`;
create table `supplies_return`(
`nid` int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '员工',
`supplies_id_id` int(11) NOT NULL COMMENT '用品',
`remark` varchar (512) NOT NULL COMMENT '归还备注',
`return_time` datetime DEFAULT NULL COMMENT '归还日期'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用品归还';

drop table if exists `supplies_return_attach`;
create table `supplies_return_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`sid_id` int(11) NOT NULL COMMENT '用品归还附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用品归还附件';

