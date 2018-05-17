drop TABLE if exists `task`;
create TABLE `task`(
`tid` int(11) primary key auto_increment, 
`title` varchar(512) NOT NUll  COMMENT '任务名称',
`content` text NOT NULL COMMENT '任务描述', 
`type_id` smallint NOT NULL COMMENT ' 任务类型',
`issuer_id` int(11) NOT NULL  COMMENT '发布人',
`perfor_id` int(11) NOT NUll COMMENT '绩效分类',
`execute_way` tinyint(1) NOT NUll DEFAULT 0 COMMENT'0代表并行执行，1次序执行',
`teamwork_auth` tinyint(1) NOT NUll DEFAULT 0 COMMENT '0代表相互可见；1互不可见；2指定可见',
`tcid`  int(11) COMMENT '任务周期类型',
`start_time` datetime  DEFAULT NULL  COMMENT '起止日期',
`deadline` datetime  DEFAULT NUll  COMMENT '终止期限',
`is_assign` tinyint(1) NOT NULL DEFAULT 0 COMMENT '指派状态：0未指派;已指派',
`is_finish` tinyint(1) NOT NULL DEFAULT 0 COMMENT '完成状态：0未完成;1已完成',
`status` tinyint(1) NOT NUll DEFAULT 1 COMMENT'1启动,2暂停,3终止',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务表';



drop TABLE if exists `performemce`;
create TABLE `performemce`(
`pid` int(11) primary key auto_increment,
`name` varchar(32) NOT NULL COMMENT '名称' unique,
`personal_score` int(11)  NOT NULL COMMENT '个人分值',
`personal_total` int(11)  NOT NULL COMMENT '个人总分'
`team_score` int(11)  NOT NULL COMMENT '个人分值',
`team_total` int(11)  NOT NULL COMMENT '个人总分'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='绩效';





drop TABLE if exists `task_type`;
create TABLE `task_type`(
`tpid` int(11) primary key auto_increment,
`name` varchar(32) NOT NULL COMMENT '名称' unique
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务类型表';



drop TABLE if exists `task_attachment`;
create TABLE `task_attachment`(
`tamid` int(11) primary key auto_increment,
`tid` int(11) NOT NULL  COMMENT '任务ID',
`attachment` varchar(512) COMMENT '附件',
`name` varchar(64) COMMENT '附件名称',
`description` varchar(512) COMMENT '附件描述'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务附件总表';


drop TABLE if exists `staff`;
create TABLE `staff`(
`sid` int(11) primary key auto_increment, 
`name` varchar(64) NOT NUll,
`department` int(11) COMMENT'部门'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='员工表';

drop TABLE if exists `department`;
create TABLE `department`(	
`id` int(11) primary key auto_increment,
`department` varchar(32) COMMENT '部分' 
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='员工部门表';

drop TABLE if exists `task_tag`;
create TABLE `task_tag`(
`ttid` int(11) NOT NULL primary key auto_increment,
`tid` int(11) NOT NULL  COMMENT '任务id',
`name` varchar(32) NOT NULL COMMENT '标签名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务标签表';
alter table task_tag  ADD UNIQUE KEY `tid_name`(`tid`,`name`) USING BTREE;

drop TABLE if exists `task_cycle`;
create TABLE `task_cycle`(
`tcid` int(11) NOT NULL  primary key auto_increment,
`name` varchar(32) NOT NULL unique
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务周期表';


drop TABLE if exists `task_assign`;
create TABLE `task_assign`(
`tasid`int(11) NOT NULL primary key auto_increment,
`tid` int(11) NOT NULL COMMENT'任务ID',
`member_id` int(11) NOT NULL COMMENT' 员工ID',
`content` text NOT NULL COMMENT '任务描述',
`deadline` datetime NOT NULL COMMENT '最后期限',
`weight` smallint(5)  NOT NULL  COMMENT '权重:0-100',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务分配表';


drop TABLE if exists `task_assign_attachment`;
create TABLE `task_assign_attachment`(
`taaid` int(11) primary key auto_increment,
`tid` int(11) NOT NULL  COMMENT '任务ID',
`sid` int(11) NOT NULL  COMMENT '员工ID',
`attachment` varchar(512) COMMENT '附件',
`description` varchar(512) COMMENT '附件描述'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务附件分配表';


drop TABLE if exists `task_auth`;
create TABLE `task_auth`(
`taid` int(11) NOT NUll primary key auto_increment,
`tmid` int(11) NOT NUll  COMMENT '任务分配ID',
`status` tinyint(1) NOT NULL COMMENT '审核状态：0 未审核，1已审核',
`result` tinyint(1) NOT NULL COMMENT '审核状态：0 通过，1未通过',
`score` tinyint(1) NOT NULL COMMENT '评分：1及格；2一般；3出色；4优秀；5经验被录取到知识库',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务审核表';


drop TABLE if exists `task_reject_record`;
create TABLE `task_reject_record`(
`trid` int(11) NOT NULL primary key auto_increment,
`tmid` int(11) NOT NULL COMMENT '任务分配ID',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`reason` text COMMENT '原因'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务驳回记录表';


drop TABLE if exists `task_submit_record`;
create TABLE `task_submit_record`(
`tsid` int(11)  primary key auto_increment,
`tmid` int(11) NOT NULL COMMENT '任务分配ID',
`title` varchar(512) COMMENT '标题',
`summary` varchar(512) COMMENT '备注',
`experience` varchar(512) COMMENT '心得',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务提交记录表';


drop TABLE if exists `task_submit_attachment`;
create TABLE `task_submit_attachment`(
`tsaid` int(11) primary key auto_increment,
`tsid`  int(11) NOT NULL COMMENT '任务提交ID',
`attachment` varchar(512) COMMENT '附件',
`description` varchar(512) COMMENT '附件描述'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务提交附件表';

drop TABLE if exists `task_review`;
create TABLE `task_review`(
`tvid`int(11) primary key auto_increment,
`tid` int(11) NOT NULL COMMENT'任务ID',
`sid` int(11) NOT NULL COMMENT '负责人ID',
`follow` tinyint(1) NOT NULL DEFAULT 0 COMMENT '次序'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务审核人';
alter table task_review  ADD UNIQUE KEY `task_staff_id`(`tid`,`sid`) USING BTREE;
