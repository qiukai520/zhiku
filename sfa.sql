drop TABLE if exists `customer_info`;
create TABLE `customer_info`(
`nid` int(11) primary key auto_increment,
`purpose_id` int (1) COMMENT '客户意向',
`category_id` smallint (6) COMMENT '客户分类',
`company` varchar (32) COMMENT '公司名称',
`industry_id` varchar (32) NOT NULL  COMMENT '所属行业',
`employees` int(11)  default 0 COMMENT '人数',
`business` varchar (64)   COMMENT '主营业务',
`introduce` varchar (512) COMMENT '公司介紹',
`website` varchar (64) COMMENT '公司网站',
`phone` varchar (16) COMMENT '公司电话',
`town_id`int(11)  NOT NUll COMMENT '街道',
`address` varchar (128) COMMENT '详细地址',
`remark` varchar (128) COMMENT '备注',
`follower_id`int(11)  DEFAULT 0  COMMENT '跟进人',
`ftime` datetime   DEFAULT NUll   COMMENT '开始跟进时间',
`recorder_id`int(11) NOT NULL COMMENT '录入人',
`is_sign` tinyint(1) NOT NULL DEFAULT 0 COMMENT '签约状态:0未签约，1已签约',
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



drop TABLE if exists `customer_linkman`;
create TABLE `customer_linkman`(
`nid` int(11) primary key auto_increment,
`customer_id` int(11) NOT NULL  COMMENT '客户',
`name` varchar(16) NOT NUll COMMENT '姓名',
`wx_name` varchar(16)  COMMENT '微信名',
`gender` tinyint(1) NOT NULL  DEFAULT 0 COMMENT '性别:0男，1女',
`age`  tinyint(1) COMMENT '年龄',
`marriage`  tinyint(1) NOT NULL  DEFAULT 0 COMMENT '婚姻:0未婚，1已婚',
`job_title` int(11) NOT NULL  COMMENT '职位',
`birthday` datetime  DEFAULT NUll  COMMENT '生日',
`is_lunar` tinyint(1)   DEFAULT 0 COMMENT '生日农历or公历:0公历，1农历',
`mobile` varchar (11) COMMENT '手机号码',
`phone` varchar (16) COMMENT '电话号码',
`ext_phone` varchar (16) COMMENT '分机号码',
`native_place` varchar (16) COMMENT '籍贯',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`remark` varchar (128) COMMENT '备注',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系人表';

drop TABLE if exists `customer_linkman_attach`;
create TABLE `customer_linkman_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`linkman_id` int(11) NOT NULL COMMENT'联系人',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系人附件';


drop TABLE if exists `customer_linkman_card`;
create TABLE `customer_linkman_card`(
`nid` int(11) primary key auto_increment,
`linkman_id` int(11) NOT NULL  COMMENT '联系人',
`photo` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系人名片';


drop TABLE if exists `customer_linkman_photo`;
create TABLE `customer_linkman_photo`(
`nid` int(11) primary key auto_increment,
`linkman_id` int(11) NOT NULL  COMMENT '联系人',
`photo` varchar(128) COMMENT '路径',
`name` varchar(64) COMMENT '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系人照片';


drop TABLE if exists `customer_memo`;
create table `customer_memo`(
`nid` int(11) primary key auto_increment,
`customer_id`int(11) NOT NULL  COMMENT '客户',
`title` varchar (128) NOT NULL  COMMENT '标题',
`detail` varchar (512) NOT NULL  COMMENT '详细',
`recorder_id`int(11) NOT NULL  COMMENT '登记人',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户备忘';


drop TABLE if exists `customer_memo_attach`;
create TABLE `customer_memo_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`memo_id` int(11) NOT NULL COMMENT'备忘',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='备忘附件';


drop TABLE if exists `follow_way`;
create TABLE `follow_way`(
`nid`int(11) NOT NULL primary key auto_increment,
`code` varchar(16) COMMENT '算法编号',
`content` varchar(128) COMMENT '跟进方式',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='跟进方式';


drop TABLE if exists `follow_contact`;
create TABLE `follow_contact`(
`nid`int(11) NOT NULL primary key auto_increment,
`code` varchar(16) COMMENT '算法编号',
`content` varchar(128) COMMENT '联系方式',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系方式';


drop TABLE if exists `follow_result`;
create TABLE `follow_result`(
`nid`int(11) NOT NULL primary key auto_increment,
`code` varchar(16) COMMENT '算法编号',
`content` varchar(128) COMMENT '客户意向',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户意向';

drop TABLE if exists `customer_purpose`;
create TABLE `customer_purpose`(
`nid`int(11) NOT NULL primary key auto_increment,
`code` varchar(16) COMMENT '算法编号',
`content` varchar(128) COMMENT '意向分类',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='意向分类';


drop TABLE if exists `customer_follow`;
create TABLE `customer_follow`(
`nid`int(11) NOT NULL primary key auto_increment,
`customer_id` int(11) NOT NULL COMMENT'客户',
`way_id` int(11) NOT NULL COMMENT'跟进方式',
`contact_id` int(11) NOT NULL COMMENT'联络方式',
`linkman_id` int(11) NOT NULL COMMENT'跟进联系人',
`result_id` int(11) NOT NULL COMMENT'客户意向',
`purpose_id` int(11) NOT NULL COMMENT'意向分类',
`next_step` varchar (512) COMMENT '下一步计划',
`detail` varchar (512) COMMENT '跟进详情',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`date` datetime  DEFAULT NUll  COMMENT '跟进日期',
`recorder_id`int(11) NOT NULL COMMENT '跟进人',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户跟进记录';



drop TABLE  if  exists `customer_contact`;
create table `customer_contact`(
`nid` int(11) primary key auto_increment,
`customer_id` int(11) NOT NULL COMMENT '客户',
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
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应商来往表';


drop TABLE if exists `c_contact_attach`;
create TABLE `c_contact_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`contact_id` int(11) NOT NULL COMMENT'客户来往',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='来往附件';

drop TABLE if exists `c_follow_attach`;
create TABLE `c_follow_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`follow_id` int(11) NOT NULL COMMENT'客户跟踪',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='跟踪附件';


drop TABLE  if  exists `wastage_goods`;
create table `wastage_goods`(
`nid` int(11) primary key auto_increment,
`goods_id` int(11) NOT NULL COMMENT '商品',
`unit_id` int (11) NOT NULL COMMENT '商品单位',
`amount` tinyint(1) NOT NULL COMMENT '数量',
`reason` varchar (128)  COMMENT '原因',
`way` varchar (64)   COMMENT '处置方式',
`proposal` varchar (128) COMMENT'改进' ,
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是',
`recorder_id`int(11) NOT NULL COMMENT '记录人',
`date`  datetime  DEFAULT NUll  COMMENT '记录日期',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品损耗';


drop TABLE if exists `wastage_attach`;
create TABLE `wastage_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`wastage_id` int(11) NOT NULL COMMENT'损耗记录',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='损耗附件';


drop TABLE if exists `wastage_solver`;
create TABLE `wastage_solver`(
`nid`int(11) NOT NULL primary key auto_increment,
`wid_id` int(11) NOT NULL COMMENT'损耗记录',
`sid_id` int(11) NOT NULL COMMENT'处理人',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='损耗处理人';



drop TABLE if exists `sea_rule`;
create TABLE `sea_rule`(
`nid`int(11) NOT NULL primary key auto_increment,
`rule` int(11) NOT NULL default 15 COMMENT'天数',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='公海法则';