

drop TABLE if exists `contract_follow`;
create TABLE `contract_follow`(
`nid`int(11) NOT NULL primary key auto_increment,
`contract_id` int(11) NOT NULL COMMENT'合同',
`way_id` int(11) NOT NULL COMMENT'跟进方式',
`contact_id` int(11) NOT NULL COMMENT'联络方式',
`linkman_id` int(11) NOT NULL COMMENT'跟进联系人',
`next_step` varchar (512) COMMENT '下一步计划',
`detail` varchar (512) COMMENT '跟进详情',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0保留，1删除',
`date` datetime  DEFAULT NUll  COMMENT '跟进日期',
`recorder_id`int(11) NOT NULL COMMENT '跟进人',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='合同跟进记录';


drop TABLE if exists `contract_follow_attach`;
create TABLE `contract_follow_attach`(
`nid`int(11) NOT NULL primary key auto_increment,
`follow_id` int(11) NOT NULL COMMENT'合同跟进',
`attachment` varchar(128) COMMENT '附件路径',
`description` varchar(128) COMMENT '附件描述',
`name` varchar(64) COMMENT '附件名称',
`is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '删除状态:0否，1是'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='合同跟进附件';