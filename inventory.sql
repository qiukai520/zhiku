
drop TABLE if exists `supplier`;
create TABLE `supplier`(
`nid` int(11) primary key auto_increment,
`customer_id` smallint (6) COMMENT '客户分类',
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


drop TABLE if exists `company_photo`;
create TABLE `staff_life_photo`(
`nid` int(11) primary key auto_increment,
`sid_id` int(11) NOT NULL  COMMENT '员工编号',
`life_photo` varchar(512) COMMENT '路径',
`name` varchar(128) COMMENT '名称',
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='生活照片';

drop TABLE if exists `customer`;
create table `customer`(
`nid` int(11) primary key auto_increment,
`customer` varchar (32) NOT NULL  COMMENT '客户分类',
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户分类';


drop TABLE if exists `industry`;
create table `industry`(
`nid` int(11) primary key auto_increment,
`industry` varchar (32) NOT NULL  COMMENT '行业',
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='行业';


drop TABLE if exists `province`;
create table `industry`(
`nid` int(11) primary key auto_increment,
`province` varchar (16) NOT NULL  COMMENT '省份',
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='省份';



drop TABLE if exists `city`;
create table `city`(
`nid` int(11) primary key auto_increment,
`city` varchar (16) NOT NULL  COMMENT '市',
`province_id` int (11) NOT NULL  COMMENT '所属省份',
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='市';


drop TABLE if exists `country`;
create table `country`(
`sid` int(11) primary key auto_increment,
`country` varchar (16) NOT NULL  COMMENT '县(区)',
`city_id` int (11) NOT NULL  COMMENT '市',
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='市';



drop TABLE if exists `linkman`;
create TABLE `linkman`(
`nid` int(11) primary key auto_increment,
`supplier_id` int(11) NOT NULL  COMMENT '供应商',
`name` varchar(16) NOT NUll COMMENT '姓名',
`sex` tinyint(1) NOT NULL  DEFAULT 0 COMMENT '性别:0男，1女',
`age`  tinyint(1) COMMENT '年龄',
`marriage`  tinyint(1) NOT NULL  DEFAULT 0 COMMENT '婚姻:0未婚，1已婚',
`birthday` datetime  COMMENT '生日',
`mobile` varchar (11) COMMENT '手机号码',
`phone` varchar (16) COMMENT '电话号码',
`native_place` varchar (16) COMMENT '籍贯',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='员工表';
