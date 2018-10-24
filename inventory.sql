
drop TABLE if exists `supplier`;
create TABLE `supplier`(
`nid` int(11) primary key auto_increment,
`category_id` smallint (6) COMMENT '供应商分类',
`company` varchar (32) COMMENT '公司名称',
`industry_id` varchar (32) NOT NULL  COMMENT '所属行业',
`employees` int(11) NOT NUll COMMENT '人数',
`product` varchar (64)  NOT NUll COMMENT '主营商品',
`introduce` varchar (512) COMMENT '公司介紹',
`website` varchar (64) COMMENT '公司网站',
`phone` varchar (16) COMMENT '公司电话',
`bank` varchar (32) COMMENT '开户银行',
`bank_account` varchar (32) COMMENT '银行账号',
`account_name` varchar (16) COMMENT '开户名',
`town_id`int(11)  NOT NUll COMMENT '街道',
`address` varchar (128) COMMENT '详细地址',
`remark` varchar (128) COMMENT '备注',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应商';


drop TABLE if exists `goods`;
create TABLE `goods`(
`nid` int(11) primary key auto_increment,
`category_id` smallint (6) COMMENT '商品分类',
`name` varchar(32) NOT NUll COMMENT '商品名称',
`description` varchar (512) COMMENT '商品描述',
`standard` varchar (32)   COMMsENT '商品规格',
`unit_id` smallint (6) COMMENT '商品单位',
`code` varchar (32) COMMENT '商品条码',
`start_month` tinyint(1)  COMMENT '起始产期:1-12月份',
`end_month` tinyint(1)   COMMENT '结束期：1-12月份',
`area`varchar(64) COMMENT '产地',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
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
`caption` varchar (16) NOT NULL  COMMENT '商品分类',
`parent_id` int(11) NOT NULL default 0 COMMENT'上级分类'
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
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系人附件';


drop TABLE if exists `linkman_card`;
create TABLE `linkman_card`(
`nid` int(11) primary key auto_increment,
`linkman_id` int(11) NOT NULL  COMMENT '联系人',
`photo` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系人名片';


drop TABLE if exists `linkman_photo`;
create TABLE `linkman_photo`(
`nid` int(11) primary key auto_increment,
`linkman_id` int(11) NOT NULL  COMMENT '联系人',
`photo` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系人照片';


drop TABLE if exists `supplier_licence`;
create TABLE `supplier_licence`(
`nid` int(11) primary key auto_increment,
`supplier_id` int(11) NOT NULL  COMMENT '运营商',
`photo` varchar(128) COMMENT '路径',
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
`photo` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品条码';


drop TABLE if exists `goods_photo`;
create TABLE `goods_photo`(
`nid` int(11) primary key auto_increment,
`goods_id` int(11) NOT NULL  COMMENT '商品编号',
`photo` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品图片';


drop TABLE if exists `supplier_memo`;
create table `supplier_memo`(
`nid` int(11) primary key auto_increment,
`supplier_id`int(11) NOT NULL  COMMENT '供应商',
`title` varchar (128) NOT NULL  COMMENT '标题',
`detail` varchar (512) NOT NULL  COMMENT '详细',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应商备忘';


drop TABLE if exists `memo_attach`;
create TABLE `memo_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`memo_id` int(11) NOT NULL COMMENT'备忘',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='备忘附件';


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
`code` int(11)  NOT NULL COMMENT '编码',
`province` varchar (16) NOT NULL  COMMENT '省份',
`nation_id` int (11)  DEFAULT 1 COMMENT '所属国家'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='省份';



drop TABLE if exists `city`;
create table `city`(
`nid` int(11) primary key auto_increment,
`code` int(11)  NOT NULL COMMENT '编码',
`city` varchar (16) NOT NULL  COMMENT '市',
`province_id` int (11) NOT NULL  COMMENT '所属省份'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='市';


drop TABLE if exists `country`;
create table `country`(
`nid` int(11) primary key auto_increment,
`code` int(11)  NOT NULL COMMENT '编码',
`country` varchar (32) NOT NULL  COMMENT '县(区)',
`city_id` int (11) NOT NULL  COMMENT '所属市区'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='市';


drop TABLE if exists `town`;
create table `town`(
`nid` int(11) primary key auto_increment,
`code` int(11)  NOT NULL COMMENT '编码',
`town` varchar (64) NOT NULL  COMMENT '街道',
`country_id` int (11) NOT NULL  COMMENT '所属县(区)'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='街道';

drop TABLE if exists `linkman`;
create TABLE `linkman`(
`nid` int(11) primary key auto_increment,
`supplier_id` int(11) NOT NULL  COMMENT '供应商',
`name` varchar(16) NOT NUll COMMENT '姓名',
`gender` tinyint(1) NOT NULL  DEFAULT 0 COMMENT '性别:0男，1女',
`age`  tinyint(1) COMMENT '年龄',
`marriage`  tinyint(1) NOT NULL  DEFAULT 0 COMMENT '婚姻:0未婚，1已婚',
`birthday` datetime  DEFAULT NUll  COMMENT '生日',
`is_lunar` tinyint(1)   DEFAULT 0 COMMENT '生日农历or公历:0公历，1农历',
`mobile` varchar (11) COMMENT '手机号码',
`phone` varchar (16) COMMENT '电话号码',
`ext_phone` varchar (16) COMMENT '分机号码',
`native_place` varchar (16) COMMENT '籍贯',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`remark` varchar (128) COMMENT '备注',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系人表';


drop TABLE  if  exists `supplier_contact`;
create table `supplier_contact`(
`nid` int(11) primary key auto_increment,
`supplier_id` int(11) NOT NULL COMMENT '供应商',
`linkman_id` int (11) NOT NULL COMMENT '联系人',
`category` tinyint(1) NOT NULL COMMENT '交易分类',
`project` varchar (64) NOT NULL COMMENT '项目名称',
`description` varchar (128)   COMMENT '项目详细',
`received`  DECIMAL (8,2) COMMENT'已收/已付金额',
`received_remark` varchar (128) COMMENT'已收/已付备注' ,
`receivable`  DECIMAL (8,2) COMMENT'应收/应付金额',
`receivable_remark` varchar (128) COMMENT'应收/应付备注' ,
`pending`  DECIMAL (8,2) COMMENT'待收/待付金额',
`pending_remark` varchar (128) COMMENT'待收/待付备注' ,
`date`  datetime  DEFAULT NUll  COMMENT '交易日期',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应商来往表';


drop TABLE if exists `contact_attach`;
create TABLE `contact_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`contact_id` int(11) NOT NULL COMMENT'供应商来往',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='来往附件';

drop TABLE if  exists `goods_price`;
create TABLE `goods_price`(
`nid` int(11) primary key auto_increment,
`goods_id` int(11) NOT NULL COMMENT '商品',
`supplier_id` int(11) NOT NULL COMMENT '供应商',
`unit_id` int(11) NOT NULL COMMENT '单位',
`amount` smallint(6)   COMMENT '数量',
`logistics` DECIMAL (8,2)  COMMENT'物流费用',
`logis_remark` varchar (128)   COMMENT '物流备注',
`price`  DECIMAL (8,2) COMMENT'单价',
`linkman_id` int (11) NOT NULL COMMENT '联系人',
`date` datetime  DEFAULT NUll  COMMENT '报价日期',
`staff_id` int (11) NOT NULL COMMENT '录入人',
`remark` varchar (128)   COMMENT '备注',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品报价';

drop table if exists `price_compare`;
create table `price_compare`(
`nid` int(11) primary key auto_increment,
`goods_id` int(11) NOT NULL  COMMENT '商品',
`unit_id` int(11) NOT NULL COMMENT '单位',
`retail_id` int(11) NOT NULL COMMENT '比价商家',
`amount` int(11) COMMENT '数量',
`price` decimal (8,2) NOT NULL COMMENT '价格',
`date` datetime  DEFAULT NUll  COMMENT '比价日期',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
`last_edit`   timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE  CURRENT_TIMESTAMP COMMENT'最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='零售比价';


drop table  if exists retail_supplier;
create table  `retail_supplier`(
`nid` int(11) primary key  auto_increment,
`caption` varchar(32) NOT NULL COMMENT'零售商'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='零售供应商';


drop TABLE if exists `price_attach`;
create TABLE `price_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`price_id` int(11) NOT NULL COMMENT'报价附件',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='报价附件';


drop TABLE if exists `warehouse`;
create TABLE `warehouse`(
`nid`int(11) NOT NULL primary key auto_increment,
`town_id` int(11) NOT NULL COMMENT'街道',
`name` varchar(64) COMMENT '仓库名称',
`address` varchar(128) COMMENT '详细地址',
`lng` decimal(10,6) COMMENT '经度',
`lat` decimal(10,6) COMMENT '纬度',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='仓库';

drop TABLE if exists `ware_location`;
create table `ware_location`(
`nid` int(11) primary key auto_increment,
`location` varchar (16) NOT NULL  COMMENT '库位',
`warehouse_id` int (11) NOT NULL  COMMENT '所属仓库'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='库位';

drop table if exists `inventory`;
create table `inventory`(
`nid` int(11) primary key auto_increment,
`goods_id` int(11) NOT NULL  COMMENT '商品',
`unit_id` int(11) NOT NULL COMMENT '单位',
`warehouse_id` int(11) NOT NULL COMMENT '所在仓库',
`recorder_id` int(11) NOT NULL COMMENT '录入人',
`batch` int(11) NOT NULL COMMENT '入库批次',
`amount` int(11) COMMENT '数量',
`date` datetime  DEFAULT NUll  COMMENT '入库日期',
`location_id` int (11)  COMMENT '库位',
`purchase_id`int(11)  COMMENT '采购单',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
`last_edit`   timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE  CURRENT_TIMESTAMP COMMENT'最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='库存';

drop TABLE if exists `inventory_attach`;
create TABLE `inventory_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`inventory_id` int(11) NOT NULL COMMENT'库存',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='报价附件';


drop table if exists `purchase`;
create table `purchase`(
`nid` int(11) primary key auto_increment,
`goods_id` int(11) NOT NULL  COMMENT '商品',
`supplier_id` int(11) NOT NULL  COMMENT '供应商',
`unit_id` int(11) NOT NULL COMMENT '单位',
`linkman_id` int(11) NOT NULL COMMENT '联系人',
`recorder_id` int(11) NOT NULL COMMENT '录入人',
`batch` int(11) NOT NULL COMMENT '采购批次',
`amount` int(11) COMMENT '数量',
`price` decimal (10,2) COMMENT '单价',
`total_price` decimal (10,2) COMMENT '总价',
`date` datetime  DEFAULT NUll  COMMENT '入库日期',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
`last_edit`   timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE  CURRENT_TIMESTAMP COMMENT'最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='库存';

drop TABLE if exists `purchase_attach`;
create TABLE `purchase_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`purchase_id` int(11) NOT NULL COMMENT'采购记录',
`attachment` varchar(128) COMMENT '凭证名称',
`description` varchar(128) COMMENT '凭证名称',
`name` varchar(64) COMMENT '凭证名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='采购凭证';
