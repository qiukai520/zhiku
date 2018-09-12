
drop TABLE if exists `supplier`;
create TABLE `supplier`(
`nid` int(11) primary key auto_increment,
`category_id` smallint (6) COMMENT '供应商分类',
`company` varchar (32) COMMENT '公司名称',
`industry_id` varchar (32) NOT NULL  COMMENT '所属行业',
`employees` int(11) NOT NUll COMMENT '人数',
`goods_id` int (11)  NOT NUll COMMENT '主营商品',
`introduce` varchar (512) COMMENT '公司介紹',
`website` varchar (64) COMMENT '公司网站',
`phone` varchar (16) COMMENT '公司电话',
`bank` varchar (32) COMMENT '开户银行',
`bank_account` varchar (32) COMMENT '银行账号',
`account_name` varchar (16) COMMENT '开户名',
`country_id`int(11)  NOT NUll COMMENT '县(区)',
`address` varchar (128) COMMENT '详细地址',
`remark` varchar (128) COMMENT '备注',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应商';


drop TABLE if exists `goods`;
create TABLE `goods`(
`nid` int(11) primary key auto_increment,
`category_id` smallint (6) COMMENT '商品分类',
`name` varchar(32) NOT NUll COMMENT '商品名称',
`description` varchar (512) COMMENT '商品描述',
`standard` varchar (32)   COMMENT '商品规格',
`unit` varchar (16) COMMENT '商品单位',
`start_time` datetime  DEFAULT NUll COMMENT '起始产期',
`end_time` datetime  DEFAULT NUll COMMENT '结束期',
`country_id`int(11)  NOT NUll COMMENT '县(区)',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品';


drop TABLE if exists `goods_unit`;
create table `goods_unit`(
`nid` int(11) primary key auto_increment,
`caption` varchar (16) NOT NULL  COMMENT '商品单位'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品单位';


drop TABLE if exists `goods_category`;
create table `goods_category`(
`nid` int(11) primary key auto_increment,
`caption` varchar (16) NOT NULL  COMMENT '商品分类'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品分类';


drop TABLE if exists `supplier_category`;
create table `supplier_category`(
`nid` int(11) primary key auto_increment,
`caption` varchar (16) NOT NULL  COMMENT '供应商分类'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应商分类';


drop TABLE if exists `industry`;
create table `industry`(
`nid` int(11) primary key auto_increment,
`industry` varchar (16) NOT NULL  COMMENT '行业'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='行业';


drop TABLE if exists `supplier_attach`;
create TABLE `supplier_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`supplier_id` int(11) NOT NULL COMMENT'供应商',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应商附件';


drop TABLE if exists `goods_attach`;
create TABLE `goods_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`goods_id` int(11) NOT NULL COMMENT'商品',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品附件';


drop TABLE if exists `linkman_attach`;
create TABLE `linkman_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`linkman_id` int(11) NOT NULL COMMENT'联系人',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品附件';

drop TABLE if exists `supplier_licence`;
create TABLE `supplier_licence`(
`nid` int(11) primary key auto_increment,
`supplier_id` int(11) NOT NULL  COMMENT '运营商',
`licence` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应商营业执照';


drop TABLE if exists `supplier_photo`;
create TABLE `supplier_photo`(
`nid` int(11) primary key auto_increment,
`supplier_id` int(11) NOT NULL  COMMENT '员工编号',
`photo` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应商照片';


drop TABLE if exists `goods_bar_code`;
create TABLE `goods_bar_code`(
`nid` int(11) primary key auto_increment,
`goods_id` int(11) NOT NULL  COMMENT '商品编号',
`bar_code` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品条码';

drop TABLE if exists `industry`;
create table `industry`(
`nid` int(11) primary key auto_increment,
`industry` varchar (32) NOT NULL  COMMENT '行业'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='行业';


drop TABLE if exists `nation`;
create table `nation`(
`nid` int(11) primary key auto_increment,
`nation` varchar (16) NOT NULL  COMMENT '国家'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='国家';

drop TABLE if exists `province`;
create table `province`(
`nid` int(11) primary key auto_increment,
`province` varchar (16) NOT NULL  COMMENT '省份',
`nation_id` int (11) NOT NULL  COMMENT '所属国家'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='省份';



drop TABLE if exists `city`;
create table `city`(
`nid` int(11) primary key auto_increment,
`city` varchar (16) NOT NULL  COMMENT '市',
`province_id` int (11) NOT NULL  COMMENT '所属省份'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='市';


drop TABLE if exists `country`;
create table `country`(
`nid` int(11) primary key auto_increment,
`country` varchar (16) NOT NULL  COMMENT '县(区)',
`city_id` int (11) NOT NULL  COMMENT '所属市区'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='市';



drop TABLE if exists `linkman`;
create TABLE `linkman`(
`nid` int(11) primary key auto_increment,
`supplier_id` int(11) NOT NULL  COMMENT '供应商',
`name` varchar(16) NOT NUll COMMENT '姓名',
`gender` tinyint(1) NOT NULL  DEFAULT 0 COMMENT '性别:0男，1女',
`age`  tinyint(1) COMMENT '年龄',
`marriage`  tinyint(1) NOT NULL  DEFAULT 0 COMMENT '婚姻:0未婚，1已婚',
`birthday` datetime  COMMENT '生日',
`mobile` varchar (11) COMMENT '手机号码',
`phone` varchar (16) COMMENT '电话号码',
`native_place` varchar (16) COMMENT '籍贯',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`remark` varchar (128) COMMENT '备注',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='员工表';
