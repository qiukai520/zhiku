drop TABLE if exists `file`;
create TABLE `file`(
`nid`int(11) NOT NULL primary key auto_increment,
`name` varchar(64) COMMENT '文件名',
`owner_id` int(11) NOT NULL COMMENT'上传者',
-- `parent_id` int(11) NOT NULL COMMENT'上级目录',
`classify` tinyint(11) NOT NULL COMMENT'文件类型',
`size` int(11) NOT NULL COMMENT'文件大小',
`path` varchar(128) COMMENT '附件路径',
`digest` varchar(128) COMMENT 'sha1 摘要',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
`last_edit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '编辑时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文件信息';

drop TABLE if exists `file_tag`;
create TABLE `file_tag`(
`nid`int(11) NOT NULL primary key auto_increment,
`name` varchar(32) NOT NULL COMMENT '标签名'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文件标签';

drop TABLE if exists `file2tag`;
create TABLE `file2tag`(
`nid`int(11) NOT NULL primary key auto_increment,
`tag_id` int(11) NOT NULL COMMENT '标签',
`file_id` int(11) NOT NULL COMMENT '标签'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文件|标签关系表';


-- drop TABLE if exists `file_directory`;
-- create TABLE `file_directory`(
-- `nid`int(11) NOT NULL primary key auto_increment,
-- `name` varchar(64) COMMENT '目录名',
-- `owner_id` int(11) NOT NULL COMMENT'上传者',
-- `parent_id` int(11) NOT NULL COMMENT'上级目录',
-- `path` varchar(128) COMMENT '路径',
-- `depart_id` int(11) NOT NULL COMMENT'所属部门'
-- )ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文件目录';


-- drop TABLE if exists `file_link`;
-- create TABLE `file_link`(
-- `nid`int(11) NOT NULL primary key auto_increment,
-- `digest` int(11) NOT NULL COMMENT 'sha1摘要',
-- `link` int(11) NOT NULL COMMENT '文件计数'
-- )ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文件引用计数';