drop TABLE if exists `contract_info`;
create TABLE `contract_info`(
`nid` int(11) primary key auto_increment,
`identifier` varchar (32) COMMENT '合同编号',
`product_id` int (11) COMMENT '产品',
`product_meal_id` int (11) COMMENT '套餐',
`sign` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '签订时间',
`start_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生效时间',
`end_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '到期时间',
`received`  DECIMAL (8,2) COMMENT'应收金额',
`receivable`  DECIMAL (8,2)  COMMENT'已收金额',
`year_limit` tinyint(1) COMMENT '年限',
`pending`  DECIMAL (8,2) default 0 COMMENT'待收金额',
`remark` varchar (128) COMMENT '备注',
`location` varchar (64) COMMENT '备注',
`customer_id`int(11) NOT NULL COMMENT '客户',
`belonger_id` int (11) COMMENT '签订人',
`helper_id` int (11) COMMENT '辅助人',
`is_approved` tinyint(1) NOT NULL DEFAULT 0 COMMENT '审批状态:0未审批，1通过，2不通过',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='合同信息';


drop TABLE if exists `product`;
create table `product`(
`nid` int(11) primary key auto_increment,
`name` varchar (16) NOT NULL  COMMENT '产品名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='产品名称';


drop TABLE if exists `product_meal`;
create table `product_meal`(
`nid` int(11) primary key auto_increment,
`product_id` int(11)  COMMENT '产品',
`name` varchar (32) NOT NULL  COMMENT '套餐名称',
`price`  DECIMAL (8,2) COMMENT '价格',
`standard` varchar (32) NOT NULL  COMMENT '规格',
`year_limit` tinyint(1) COMMENT '年限',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='产品套餐';

drop TABLE if exists `contract_attach`;
create TABLE `contract_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`contract_id` int(11) NOT NULL COMMENT'合同',
`attachment` varchar(128) COMMENT '合同路径',
`description` varchar(128) COMMENT '合同描述',
`name` varchar(64) COMMENT '合同名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='合同附件';

drop TABLE if exists `approver`;
create table `approver`(
`nid` int(11) primary key auto_increment,
`approver_id` varchar (16) NOT NULL  COMMENT '合同审批人',
`follow` tinyint(1) NOT NULL DEFAULT 0 COMMENT '审核顺序'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='合同审批人';
-- alter table approver  ADD UNIQUE KEY `apr_saf_id`(`approver_id`,) USING BTREE;


drop TABLE if exists `approver_result`;
create table `approver_result`(
`nid` int(11) primary key auto_increment,
`contract_id` varchar (16) NOT NULL  COMMENT '合同',
`approver_id` varchar (16) NOT NULL  COMMENT '合同审批人',
`follow` tinyint(1) NOT NULL DEFAULT 0 COMMENT '审核顺序',
`result` tinyint(1) NOT NULL DEFAULT 0 COMMENT '审核结果 0未审核,1通过,2不通过'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='合同审核结果';


drop TABLE if exists `approver_record`;
create table `approver_record`(
`nid` int(11) primary key auto_increment,
`result2` tinyint(1) NOT NULL DEFAULT 0 COMMENT '审核结果 0未审核,1通过,2不通过',
`content` varchar (1)   COMMENT '审核审核内容',
`result_id` int(1)  COMMENT'审核记录',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='审核记录';