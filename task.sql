

drop TABLE if exists `task`;
create TABLE `task`(
`tid` int(11) primary key auto_increment,
`title` varchar(512) NOT NUll  COMMENT '任务名称',
`content` text NOT NULL COMMENT '任务描述',
`type_id` smallint NOT NULL COMMENT ' 任务类型',
`issuer_id` int(11) NOT NULL  COMMENT '发布人',
`status` tinyint(1) NOT NUll DEFAULT 1 COMMENT'1启动,2暂停,3取消',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务表';


drop TABLE if exists `task_map`;
create TABLE `task_map`(
`tmid` int(11) primary key auto_increment,
`tid_id` int(11) NOT NULL  COMMENT '任务ID',
`title` varchar(512) NOT NUll  COMMENT '任务名称',
`content` text NOT NULL COMMENT '任务描述',
`type_id` smallint NOT NULL COMMENT ' 任务类型',
`perfor_id` int(11) NOT NUll COMMENT '绩效分类',
`assigner_id` int(11) NOT NULL  COMMENT '指派人',
`cycle_id`  int(11) NOT NULL  COMMENT '任务周期类型',
`start_time` datetime  DEFAULT NULL  COMMENT '起止日期',
`deadline` datetime  DEFAULT NUll  COMMENT '单次终止期限',
`project_deadline` datetime  DEFAULT NUll  COMMENT '项目终止期限',
`remark` varchar(512) NOT NUll  COMMENT '备注',
`execute_way` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0代表并行执行，1次序执行',
`teamwork_auth` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0代表相互可见；1互不可见；2指定可见',
`is_finish` tinyint(1) NOT NULL DEFAULT 0 COMMENT '完成状态：0未完成;1已完成',
`team` tinyint(1) NOT NULL DEFAULT 0 COMMENT '任务方式：0个人任务;1组队任务',
`status` tinyint(1) NOT NUll DEFAULT 1 COMMENT'1启动,2暂停,3终止',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务指派';


drop TABLE if exists `performance`;
create TABLE `performance`(
`pid` int(11) primary key auto_increment,
`name` varchar(32) NOT NULL COMMENT '名称' unique,
`personal_score` int(11)  NOT NULL COMMENT '个人分值',
`personal_total` int(11)  NOT NULL COMMENT '个人总分',
`team_score` int(11)  NOT NULL COMMENT '团队分值',
`team_total` int(11)  NOT NULL COMMENT '团队总分'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='绩效';




drop TABLE if exists `performance_record`;
create TABLE `performance_record`(
`prid` int(11) primary key auto_increment,
`sid_id` int(11)  NOT NULL COMMENT '员工',
`tmid_id` int(11)  NOT NULL COMMENT '任务',
`personal_score` int(11)  NOT NULL COMMENT '个人分值',
`team_score` int(11)  NOT NULL COMMENT '团队分值',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务绩效记录';
alter table performance_record  ADD UNIQUE KEY `sid_tmid`(`sid_id`,`tmid_id`) USING BTREE;

drop TABLE if exists `task_type`;
create TABLE `task_type`(
`tpid` smallint() primary key auto_increment,
`name` varchar(32) NOT NULL COMMENT '名称' unique
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务类型表';



drop TABLE if exists `task_attachment`;
create TABLE `task_attachment`(
`tamid` int(11) primary key auto_increment,
`tid` int(11) NOT NULL  COMMENT '任务ID',
`attachment` varchar(512) COMMENT '附件',
`name` varchar(128) COMMENT '附件名称',
`description` varchar(512) COMMENT '附件描述'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务附件总表';


drop TABLE if exists `task_map_attachment`;
create TABLE `task_map_attachment`(
`tmaid` int(11) primary key auto_increment,
`tmid_id` int(11) NOT NULL  COMMENT '任务指派编号',
`attachment` varchar(512) COMMENT '附件',
`name` varchar(128) COMMENT '附件名称',
`description` varchar(512) COMMENT '附件描述'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务指派附件总表';


drop TABLE if exists `staff`;
create TABLE `staff`(
`sid` int(11) primary key auto_increment,
`job_number` varchar (32) NOT NULL  COMMENT '工号',
`user_id`  int(11)   COMMENT '用户ID',
`name` varchar(16) NOT NUll COMMENT '员工姓名',
`life_photo` varchar (128) COMMENT '生活照片',
`sex` tinyint(1) NOT NULL  DEFAULT 0 COMMENT '性别:0男，1女',
`phone` varchar (128) COMMENT '手机号码',
`email` varchar (32) COMMENT '邮箱',
`company` varchar (32) COMMENT '公司名称',
`project` varchar (32) COMMENT '公司名称',
`department_id` int(11) COMMENT'所属部门',
`job_rank` varchar (32) COMMENT '职级',
`birthday` datetime  COMMENT '生日',
`is_lunar` tinyint(1)   DEFAULT 0 COMMENT '生日农历or公历:0公历，1农历',
`hire_day` datetime  COMMENT '入职时间',
`native_place` varchar (16) COMMENT '籍贯',
`nationality` varchar (32) COMMENT '民族',
`family_address` varchar (128) COMMENT '家庭住址',
`current_address` varchar (128) COMMENT '现住地址',
`education` varchar (16) COMMENT '学历',
`id_card` varchar (18) NOT NULL COMMENT '身份证号码',
`bank` varchar (32) COMMENT '开户银行',
`bank_account` varchar (32) COMMENT '银行账号',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='员工表';
ALTER TABLE `staff` ADD UNIQUE (
`user_id`,`job_number`,
)



drop TABLE if exists `department`;
create TABLE `department`(
`id` int(11) primary key auto_increment,
`department` varchar(32) COMMENT '部分'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='员工部门表';
ALTER TABLE `department` ADD UNIQUE (
`department`
)
drop TABLE if exists `task_tag`;
create TABLE `task_tag`(
`ttid` int(11) NOT NULL primary key auto_increment,
`tid` int(11) NOT NULL  COMMENT '任务id',
`name` varchar(32) NOT NULL COMMENT '标签名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务标签表';
alter table task_tag  ADD UNIQUE KEY `tid_name`(`tid`,`name`) USING BTREE;


drop TABLE if exists `task_map_tag`;
create TABLE `task_map_tag`(
`tmtid` int(11) NOT NULL primary key auto_increment,
`tmid_id` int(11) NOT NULL  COMMENT '任务指派编号',
`name` varchar(32) NOT NULL COMMENT '指派标签名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务标签表';
alter table task_map_tag  ADD UNIQUE KEY `tmid_name`(`tmid`,`name`) USING BTREE;


drop TABLE if exists `task_assign_tag`;
create TABLE `task_assign_tag`(
`tatid` int(11) NOT NULL primary key auto_increment,
`tasid` int(11) NOT NULL  COMMENT '任务分配ID',
`name` varchar(32) NOT NULL COMMENT '标签名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务标签表';
alter table task_assign_tag  ADD UNIQUE KEY `tid_name`(`tasid`,`name`) USING BTREE;


drop TABLE if exists `task_submit_tag`;
create TABLE `task_submit_tag`(
`tstid` int(11) NOT NULL primary key auto_increment,
`tsid` int(11) NOT NULL  COMMENT '任务提交ID',
`name` varchar(32) NOT NULL  COMMENT '标签名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务提交标签表';
alter table task_submit_tag  ADD UNIQUE KEY `tstid_name`(`tsid`,`name`) USING BTREE;


drop TABLE if exists `task_cycle`;
create TABLE `task_cycle`(
`tcid` int(11) NOT NULL  primary key auto_increment,
`name` varchar(32) NOT NULL UNIQUE
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务周期表';


drop TABLE if exists `task_assign`;
create TABLE `task_assign`(
`tasid`int(11) NOT NULL primary key auto_increment,
`tmid_id` int(11) NOT NULL COMMENT'任务ID',
`member_id_id` int(11) NOT NULL COMMENT' 员工ID',
`title`  varchar(32)  COMMENT '标题',
`content` text   COMMENT '任务描述',
`deadline` datetime  DEFAULT NUll COMMENT '最后期限',
`progress` tinyint(1)   COMMENT '进度:0-100',
`is_finish` tinyint(1)  NOT NULL  DEFAULT 0 COMMENT '完成状态：0未完成;1已完成',
`status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '任务状态:0取消，1进行中，2，暂停',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除，1保留'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务分配表';
alter table task_assign  ADD UNIQUE KEY `task_member_id`(`tmid_id`,`member_id_id`) USING BTREE;


drop TABLE if exists `task_assign_attach`;
create TABLE `task_assign_attach`(
`taaid`int(11) NOT NULL primary key auto_increment,
`tasid` int(11) NOT NULL COMMENT'任务分配ID',
`attachment` varchar(512) COMMENT '附件路径',
`description` varchar(512) COMMENT '附件描述',
`name` varchar(128) COMMENT '附件名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务分配附件表';



drop TABLE if exists `task_auth`;
create TABLE `task_auth`(
`taid` int(11) NOT NUll primary key auto_increment,
`tasid` int(11) NOT NUll  COMMENT '任务分配ID',
`status` tinyint(1) NOT NULL COMMENT '审核状态：0 未审核，1已审核',
`result` tinyint(1) NOT NULL COMMENT '审核状态：0 通过，1未通过',
`score` tinyint(1) NOT NULL COMMENT '评分：1及格；2一般；3出色；4优秀；5经验被录取到知识库',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务审核表';


drop TABLE if exists `task_review_record`;
create TABLE `task_review_record`(
`trrid` int(11) NOT NULL primary key auto_increment,
`tasid` int(11) NOT NULL COMMENT '任务分配ID',
`tvid`  int(11) NOT NULL COMMENT '任务审核ID',
`is_complete` tinyint(1)  COMMENT '是否通过',
`reason` text COMMENT '原因',
`comment`text COMMENT '评语',
`evaluate` decimal (2,1) COMMENT '评价:1.0-5.0',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务审核记录表';


drop TABLE if exists `task_submit_record`;
create TABLE `task_submit_record`(
`tsid` int(11)  primary key auto_increment,
`tasid_id` int(11) NOT NULL COMMENT '任务分配ID',
`title` varchar(512) COMMENT '标题',
`summary` varchar(512) COMMENT '总结',
`is_assist` tinyint(1) NOT NUll DEFAULT 0 COMMENT'寻求协助:0否,1是',
`remark` varchar(512) COMMENT '备注',
`completion`  int(3) NOT NUll DEFAULT 0 COMMENT'完成度：1-100',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务提交记录表';


drop TABLE if exists `task_submit_attachment`;
create TABLE `task_submit_attachment`(
`tsaid` int(11) primary key auto_increment,
`tsid`  int(11) NOT NULL COMMENT '任务提交ID',
`attachment` varchar(512) COMMENT '附件',
`name` varchar(128) COMMENT '附件名称',
`description` varchar(512) COMMENT '附件描述'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务提交附件表';

drop TABLE if exists `task_review`;
create TABLE `task_review`(
`tvid`int(11) primary key auto_increment,
`tmid_id` int(11) NOT NULL COMMENT'任务ID',
`sid_id` int(11) NOT NULL COMMENT '负责人ID',
`follow` tinyint(1) NOT NULL DEFAULT 0 COMMENT '次序',
`delete_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '删除状态:0删除,1保留'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务审核人';
alter table task_review  ADD UNIQUE KEY `task_staff_id`(`tmid`,`sid_id`) USING BTREE;


