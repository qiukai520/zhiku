drop TABLE if exists `customer_info`;
create TABLE `customer_info`(
`nid` int(11) primary key auto_increment,
`purpose` tinyint (1) COMMENT '意向分类',
`category_id` smallint (6) COMMENT '客户分类',
`company` varchar (32) COMMENT '公司名称',
`industry_id` varchar (32) NOT NULL  COMMENT '所属行业',
`employees` int(11) NOT NUll default 0 COMMENT '人数',
`business` varchar (64)   COMMENT '主营业务',
`introduce` varchar (512) COMMENT '公司介紹',
`website` varchar (64) COMMENT '公司网站',
`phone` varchar (16) COMMENT '公司电话',
`town_id`int(11)  NOT NUll COMMENT '街道',
`address` varchar (128) COMMENT '详细地址',
`remark` varchar (128) COMMENT '备注',
`recorder_id`int(11) NOT NULL COMMENT '录入人',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户信息';

drop TABLE if exists `customer_category`;
create table `customer_category`(
`nid` int(11) primary key auto_increment,
`caption` varchar (16) NOT NULL  COMMENT '客户分类'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户分类';


drop TABLE if exists `customer_attach`;
create TABLE `customer_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`customer_id` int(11) NOT NULL COMMENT'客户',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户附件';

drop TABLE if exists `customer_licence`;
create TABLE `customer_licence`(
`nid` int(11) primary key auto_increment,
`customer_id` int(11) NOT NULL  COMMENT '客户',
`photo` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户营业执照';


drop TABLE if exists `customer_photo`;
create TABLE `customer_photo`(
`nid` int(11) primary key auto_increment,
`customer_id` int(11) NOT NULL  COMMENT '客户',
`photo` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户照片';

