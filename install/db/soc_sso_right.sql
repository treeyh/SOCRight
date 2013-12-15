/*
Navicat MySQL Data Transfer

Source Database       : SOCRight

Target Server Type    : MYSQL
Target Server Version : 50169
File Encoding         : 65001

Date: 2013-12-03 19:19:25
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `sso_application`
-- ----------------------------
DROP TABLE IF EXISTS `sso_application`;
CREATE TABLE `sso_application` (
  `code` varchar(32) NOT NULL COMMENT '编号,唯一',
  `name` varchar(32) DEFAULT NULL,
  `developer` varchar(32) DEFAULT NULL COMMENT '开发人员',
  `url` varchar(256) DEFAULT NULL COMMENT '应用Url',
  `status` int(11) DEFAULT NULL COMMENT '1可用，2不可用',
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`code`),
  KEY `index_sso_application_status` (`status`),
  KEY `index_sso_application_isdelete` (`isDelete`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_application
-- ----------------------------
INSERT INTO `sso_application` VALUES ('SOCProject', '云海项目管理系统', 'Tree', 'http://pm.socsoft.net/Admin', '1', '', '2', 'Tree', '2012-07-11 21:42:16', 'Tree', '2013-08-26 10:45:10');
INSERT INTO `sso_application` VALUES ('SOCRight', '云海权限管理系统', 'Tree', 'http://ssoadmin.socsoft.net/Admin/Main', '1', '1234', '2', 'Tree', '2012-06-20 10:15:43', 'Tree', '2013-09-05 10:02:32');

-- ----------------------------
-- Table structure for `sso_department`
-- ----------------------------
DROP TABLE IF EXISTS `sso_department`;
CREATE TABLE `sso_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL COMMENT '部门名称',
  `status` int(11) DEFAULT NULL COMMENT '1可用，2不可用',
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_department
-- ----------------------------
INSERT INTO `sso_department` VALUES ('1', '技术研发部', '1', '11', '2', 'Tree', '2013-05-15 15:48:22', 'Tree', '2013-05-21 17:29:15');
INSERT INTO `sso_department` VALUES ('2', '运营支撑部', '1', '2', '2', 'Tree', '2013-05-15 16:05:29', 'Tree', '2013-05-15 16:05:29');
INSERT INTO `sso_department` VALUES ('3', '市场部', '1', '', '2', 'Tree', '2013-08-26 11:16:08', 'Tree', '2013-09-28 11:29:57');

-- ----------------------------
-- Table structure for `sso_func`
-- ----------------------------
DROP TABLE IF EXISTS `sso_func`;
CREATE TABLE `sso_func` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `appCode` varchar(32) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `code` varchar(32) DEFAULT NULL COMMENT '编号',
  `parentID` int(11) DEFAULT NULL,
  `path` varchar(1024) DEFAULT NULL,
  `customJson` text COMMENT '用户自定义权限json[{"name":"xxxx2"},{"name":"xxxx2"}]',
  `sort` int(11) DEFAULT NULL COMMENT '排序',
  `status` int(11) DEFAULT NULL COMMENT '1可用，2不可用',
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_sso_func_parentID` (`parentID`),
  KEY `index_sso_func_appCode` (`appCode`),
  KEY `index_sso_func_path` (`path`(255)),
  KEY `index_sso_func_status` (`status`),
  KEY `index_sso_func_isdelete` (`isDelete`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_func
-- ----------------------------
INSERT INTO `sso_func` VALUES ('9', 'SOCRight', '应用管理', 'AppManager', '0', 'SOCRight.AppManager', '', '1', '1', '', '2', 'Tree', '2012-07-09 10:14:03', 'Tree', '2012-07-09 10:14:03');
INSERT INTO `sso_func` VALUES ('10', 'SOCRight', '功能管理', 'FuncManager', '0', 'SOCRight.FuncManager', '', '1', '1', '', '2', 'Tree', '2012-07-09 10:14:35', 'Tree', '2013-09-26 18:26:40');
INSERT INTO `sso_func` VALUES ('11', 'SOCRight', '用户管理', 'UserManager', '0', 'SOCRight.UserManager', '[{\"k\":\"Export\",\"v\":\"导出用户数据\"},{\"k\":\"ResetPassword\",\"v\":\"重置用户密码\"},{\"k\":\"Lock\",\"v\":\"锁定用户\"}]', '0', '1', '', '2', 'Tree', '2012-07-09 10:14:58', 'Tree', '2013-08-26 16:42:28');
INSERT INTO `sso_func` VALUES ('12', 'SOCRight', '用户组管理', 'UserGroupManager', '0', 'SOCRight.UserGroupManager', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:15:26', 'Tree', '2012-07-09 10:15:26');
INSERT INTO `sso_func` VALUES ('13', 'SOCRight', '角色管理', 'RoleManager', '0', 'SOCRight.RoleManager', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:15:51', 'Tree', '2012-07-09 10:15:51');
INSERT INTO `sso_func` VALUES ('14', 'SOCRight', '用户绑定角色管理', 'UserBindRoleManager', '11', 'SOCRight.UserManager.UserBindRoleManager', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:17:52', 'Tree', '2012-07-09 10:17:52');
INSERT INTO `sso_func` VALUES ('15', 'SOCRight', '用户组绑定角色管理', 'UserGroupBindRoleManager', '12', 'SOCRight.UserGroupManager.UserGroupBindRoleManager', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:25:39', 'Tree', '2012-07-09 10:25:39');
INSERT INTO `sso_func` VALUES ('16', 'SOCRight', '用户组绑定用户管理', 'UserGroupBindUserManager', '12', 'SOCRight.UserGroupManager.UserGroupBindUserManager', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:27:58', 'Tree', '2012-07-09 10:27:58');
INSERT INTO `sso_func` VALUES ('17', 'SOCRight', '角色绑定权限管理', 'RoleBindRightManager', '13', 'SOCRight.RoleManager.RoleBindRightManager', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:39:13', 'Tree', '2012-07-09 10:39:13');
INSERT INTO `sso_func` VALUES ('18', 'SOCRight', '登录操作', 'Login', '0', 'SOCRight.Login', '[{\"k\":\"a1\",\"v\":\"xxx功能\"},{\"k\":\"a2\",\"v\":\"yyy功能\"}]', '3', '1', '', '2', 'Tree', '2012-07-10 04:00:12', 'Tree', '2013-04-26 10:36:36');
INSERT INTO `sso_func` VALUES ('190', 'SOCRight', '部门管理', 'DepartmentManager', '0', 'SOCRight.DepartmentManager', '', '0', '1', '', '2', 'Tree', '2013-07-22 14:48:26', 'Tree', '2013-07-22 14:48:26');
INSERT INTO `sso_func` VALUES ('192', 'SOCRight', '操作日志管理', 'OperLogManager', '0', 'SOCRight.OperLogManager', '[{\"k\":\"Export\",\"v\":\"导出操作数据2\"}]', '0', '1', '', '2', 'Tree', '2013-08-26 14:50:01', 'Tree', '2013-09-28 11:50:41');

-- ----------------------------
-- Table structure for `sso_log`
-- ----------------------------
DROP TABLE IF EXISTS `sso_log`;
CREATE TABLE `sso_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `operID` int(11) DEFAULT NULL,
  `appCode` varchar(32) DEFAULT NULL,
  `funcID` int(11) DEFAULT NULL,
  `action` varchar(64) DEFAULT NULL,
  `ext1` int(11) DEFAULT NULL,
  `ext2` int(11) DEFAULT NULL,
  `ext3` int(11) DEFAULT NULL,
  `ext4` int(11) DEFAULT NULL,
  `ext5` varchar(63) DEFAULT NULL,
  `ext6` varchar(512) DEFAULT NULL,
  `ext7` varchar(8192) DEFAULT NULL,
  `remark` text,
  `operTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_log
-- ----------------------------

-- ----------------------------
-- Table structure for `sso_oper_log`
-- ----------------------------
DROP TABLE IF EXISTS `sso_oper_log`;
CREATE TABLE `sso_oper_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `operID` int(11) DEFAULT NULL COMMENT '操作人ID',
  `operUserName` varchar(64) DEFAULT NULL COMMENT '操作人用户名',
  `operRealName` varchar(64) DEFAULT NULL COMMENT '操作人姓名',
  `appCode` varchar(32) DEFAULT NULL COMMENT '操作应用编号',
  `funcPath` varchar(1024) DEFAULT NULL COMMENT '功能path',
  `action` varchar(64) DEFAULT NULL COMMENT '动作',
  `targetType` int(11) DEFAULT NULL COMMENT '目标类型',
  `targetID` varchar(64) DEFAULT NULL COMMENT '目标ID',
  `targetName` varchar(64) DEFAULT NULL COMMENT '目标名称',
  `startStatus` text COMMENT '原始状态',
  `endStatus` text COMMENT '结束状态',
  `operIp` varchar(64) DEFAULT NULL COMMENT '操作IP',
  `operTime` datetime DEFAULT NULL COMMENT '操作时间',
  PRIMARY KEY (`id`),
  KEY `index_sso_oper_log_operID` (`operID`),
  KEY `index_sso_oper_log_operUserName` (`operUserName`),
  KEY `index_sso_oper_log_appCode` (`appCode`),
  KEY `index_sso_oper_log_funcPath` (`funcPath`(255)),
  KEY `index_sso_oper_log_action` (`action`),
  KEY `index_sso_oper_log_operTime` (`operTime`),
  KEY `index_sso_oper_log_targetID` (`targetID`),
  KEY `index_sso_oper_log_operIp` (`operIp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_oper_log
-- ----------------------------
INSERT INTO `sso_oper_log` VALUES ('174', '1', 'Tree', '张三', 'SOCRight', '', 'userLogin', '0', '', '', '', '', '180.168.5.182', '2013-11-25 15:01:40');
INSERT INTO `sso_oper_log` VALUES ('175', '1', 'Tree', '张三', 'SOCRight', '', 'userLogin', '0', '', '', '', '', '180.168.5.182', '2013-11-25 15:01:54');
INSERT INTO `sso_oper_log` VALUES ('176', '1', 'Tree', '张三', 'SOCRight', '', 'userLogin', '0', '', '', '', '', '180.168.5.182', '2013-11-25 15:02:32');
INSERT INTO `sso_oper_log` VALUES ('177', '1', 'Tree', '张三', 'SOCRight', '', 'userLogin', '0', '', '', '', '', '180.168.5.182', '2013-11-25 15:02:37');
INSERT INTO `sso_oper_log` VALUES ('178', '1', 'Tree', '张三', 'SOCRight', '', 'userLogin', '0', '', '', '', '', '180.168.5.182', '2013-11-25 15:35:48');
INSERT INTO `sso_oper_log` VALUES ('179', '1', 'Tree', '张三', 'SOCRight', '', 'userLogin', '0', '', '', '', '', '180.168.5.182', '2013-11-25 15:36:13');
INSERT INTO `sso_oper_log` VALUES ('180', '1', 'Tree', '张三', 'SOCRight', '', 'userLogin', '0', '', '', '', '', '180.168.5.182', '2013-11-25 15:40:50');
INSERT INTO `sso_oper_log` VALUES ('181', '1', 'Tree', '张三', 'SOCProject', '', 'userLogin', '0', '', '', '', '', '180.168.5.182', '2013-11-26 09:26:06');
INSERT INTO `sso_oper_log` VALUES ('182', '1', 'Tree', '张三', 'SOCRight', '', 'userLogin', '0', '', '', '', '', '180.168.5.182', '2013-11-26 09:26:25');

-- ----------------------------
-- Table structure for `sso_role`
-- ----------------------------
DROP TABLE IF EXISTS `sso_role`;
CREATE TABLE `sso_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `status` int(11) DEFAULT NULL COMMENT '1可用，2不可用',
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_sso_role_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_role
-- ----------------------------
INSERT INTO `sso_role` VALUES ('1', '超级管理员', '1', '', '2', 'Tree', '2012-07-10 03:56:13', 'Tree', '2012-07-10 03:56:13');

-- ----------------------------
-- Table structure for `sso_role_right`
-- ----------------------------
DROP TABLE IF EXISTS `sso_role_right`;
CREATE TABLE `sso_role_right` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `funcID` int(11) DEFAULT NULL,
  `appCode` varchar(32) DEFAULT NULL,
  `roleID` int(11) DEFAULT NULL,
  `right` int(11) DEFAULT NULL,
  `customRight` varchar(4096) DEFAULT NULL,
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_sso_role_right_appCode` (`appCode`),
  KEY `index_sso_role_right_roleid` (`roleID`),
  KEY `index_sso_role_right_funcid` (`funcID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_role_right
-- ----------------------------
INSERT INTO `sso_role_right` VALUES ('1', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 03:57:02', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('2', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 03:57:02', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('3', '11', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 03:57:02', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('4', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 03:57:02', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('5', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 03:57:02', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('6', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 03:57:02', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('7', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 03:57:02', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('8', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 03:57:02', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('9', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 03:57:02', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('10', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('11', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('12', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('13', '11', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('14', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('15', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('16', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('17', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('18', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('19', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:00:25', 'Tree', '2012-07-10 04:41:44');
INSERT INTO `sso_role_right` VALUES ('20', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('21', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('22', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('23', '11', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('24', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('25', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('26', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('27', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('28', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('29', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 04:41:44', 'Tree', '2012-07-10 05:30:50');
INSERT INTO `sso_role_right` VALUES ('30', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('31', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('32', '10', 'SOCRight', '1', '15', ',1,2,', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('33', '11', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('34', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('35', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('36', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('37', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('38', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('39', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-10 05:30:51', 'Tree', '2012-07-11 22:00:29');
INSERT INTO `sso_role_right` VALUES ('40', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('41', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('42', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('43', '11', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('44', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('45', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('46', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('47', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('48', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('49', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:29', 'Tree', '2012-07-11 22:00:48');
INSERT INTO `sso_role_right` VALUES ('50', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('51', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('52', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('53', '11', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('54', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('55', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('56', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('57', '16', 'SOCRight', '1', '7', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('58', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('59', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 22:00:48', 'Tree', '2012-07-11 23:11:05');
INSERT INTO `sso_role_right` VALUES ('60', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('61', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('62', '10', 'SOCRight', '1', '15', ',1,2,', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('63', '11', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('64', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('65', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('66', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('67', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('68', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('69', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-11 23:11:05', 'Tree', '2012-07-16 14:31:59');
INSERT INTO `sso_role_right` VALUES ('71', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('72', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('73', '10', 'SOCRight', '1', '15', ',1,2,', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('74', '11', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('75', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('76', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('77', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('78', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('79', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('80', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2012-07-16 14:31:59', 'Tree', '2013-07-22 14:50:05');
INSERT INTO `sso_role_right` VALUES ('1342', '18', 'SOCRight', '9', '15', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1343', '9', 'SOCRight', '9', '0', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1344', '10', 'SOCRight', '9', '0', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1345', '11', 'SOCRight', '9', '0', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1346', '14', 'SOCRight', '9', '0', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1347', '12', 'SOCRight', '9', '0', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1348', '15', 'SOCRight', '9', '0', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1349', '16', 'SOCRight', '9', '0', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1350', '13', 'SOCRight', '9', '0', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1351', '17', 'SOCRight', '9', '0', '', '1', 'xuezhiyu', '2013-03-14 08:49:49', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1352', '18', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1353', '9', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1354', '10', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1355', '11', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1356', '14', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1357', '12', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1358', '15', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1359', '16', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1360', '13', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1361', '17', 'SOCRight', '9', '0', '', '2', 'xuezhiyu', '2013-03-14 08:51:09', 'xuezhiyu', '2013-03-14 08:51:09');
INSERT INTO `sso_role_right` VALUES ('1656', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1657', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1658', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1659', '11', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1660', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1661', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1662', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1663', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1664', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1665', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1666', '190', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-07-22 14:50:05', 'Tree', '2013-08-12 15:43:49');
INSERT INTO `sso_role_right` VALUES ('1667', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1668', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1669', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1670', '11', 'SOCRight', '1', '15', ',Export,ResetPassword,', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1671', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1672', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1673', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1674', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1675', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1676', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1677', '190', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 15:43:49', 'Tree', '2013-08-12 16:09:17');
INSERT INTO `sso_role_right` VALUES ('1678', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1679', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1680', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1681', '11', 'SOCRight', '1', '15', ',Export,', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1682', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1683', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1684', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1685', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1686', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1687', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1688', '190', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:09:17', 'Tree', '2013-08-12 16:14:23');
INSERT INTO `sso_role_right` VALUES ('1689', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1690', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1691', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1692', '11', 'SOCRight', '1', '15', ',ResetPassword,', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1693', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1694', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1695', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1696', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1697', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1698', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1699', '190', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-12 16:14:23', 'Tree', '2013-08-26 14:52:54');
INSERT INTO `sso_role_right` VALUES ('1700', '18', 'SOCRight', '17', '15', ',a1,a2,', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1701', '9', 'SOCRight', '17', '15', '', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1702', '10', 'SOCRight', '17', '15', '', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1703', '11', 'SOCRight', '17', '15', ',Export,ResetPassword,', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1704', '14', 'SOCRight', '17', '15', '', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1705', '12', 'SOCRight', '17', '15', '', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1706', '15', 'SOCRight', '17', '15', '', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1707', '16', 'SOCRight', '17', '15', '', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1708', '13', 'SOCRight', '17', '15', '', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1709', '17', 'SOCRight', '17', '15', '', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1710', '190', 'SOCRight', '17', '15', '', '1', 'Tree', '2013-08-26 13:16:26', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1711', '18', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1712', '9', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1713', '10', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1714', '11', 'SOCRight', '1', '15', ',Export,ResetPassword,', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1715', '14', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1716', '12', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1717', '15', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1718', '16', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1719', '13', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1720', '17', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1721', '190', 'SOCRight', '1', '15', '', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1722', '192', 'SOCRight', '1', '15', ',Export,', '1', 'Tree', '2013-08-26 14:52:55', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1723', '18', 'SOCRight', '1', '15', ',a1,a2,', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1724', '9', 'SOCRight', '1', '15', '', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1725', '10', 'SOCRight', '1', '15', '', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1726', '11', 'SOCRight', '1', '15', ',Export,ResetPassword,Lock,', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1727', '14', 'SOCRight', '1', '15', '', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1728', '12', 'SOCRight', '1', '15', '', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1729', '15', 'SOCRight', '1', '15', '', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1730', '16', 'SOCRight', '1', '15', '', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1731', '13', 'SOCRight', '1', '15', '', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1732', '17', 'SOCRight', '1', '15', '', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1733', '190', 'SOCRight', '1', '15', '', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1734', '192', 'SOCRight', '1', '15', ',Export,', '2', 'Tree', '2013-08-26 16:46:47', 'Tree', '2013-08-26 16:46:47');
INSERT INTO `sso_role_right` VALUES ('1735', '18', 'SOCRight', '17', '15', ',a1,a2,', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1736', '9', 'SOCRight', '17', '15', '', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1737', '10', 'SOCRight', '17', '15', '', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1738', '11', 'SOCRight', '17', '15', ',Export,ResetPassword,', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1739', '14', 'SOCRight', '17', '15', '', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1740', '12', 'SOCRight', '17', '15', '', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1741', '15', 'SOCRight', '17', '15', '', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1742', '16', 'SOCRight', '17', '15', '', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1743', '13', 'SOCRight', '17', '15', '', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1744', '17', 'SOCRight', '17', '15', '', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1745', '190', 'SOCRight', '17', '15', '', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1746', '192', 'SOCRight', '17', '3', ',Export,', '2', 'Tree', '2013-09-26 18:53:08', 'Tree', '2013-09-26 18:53:08');
INSERT INTO `sso_role_right` VALUES ('1747', '18', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1748', '9', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1749', '10', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1750', '11', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1751', '14', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1752', '12', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1753', '15', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1754', '16', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1755', '13', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1756', '17', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1757', '190', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');
INSERT INTO `sso_role_right` VALUES ('1758', '192', 'SOCRight', '16', '0', '', '2', 'Tree', '2013-10-10 14:50:51', 'Tree', '2013-10-10 14:50:51');

-- ----------------------------
-- Table structure for `sso_user`
-- ----------------------------
DROP TABLE IF EXISTS `sso_user`;
CREATE TABLE `sso_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `passWord` varchar(32) DEFAULT NULL,
  `realName` varchar(64) DEFAULT NULL,
  `parentID` int(11) DEFAULT NULL,
  `departmentID` int(11) DEFAULT NULL COMMENT '部门ID',
  `mobile` varchar(32) DEFAULT NULL,
  `tel` varchar(32) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `lastLoginTime` datetime DEFAULT NULL,
  `lastLoginApp` varchar(32) DEFAULT NULL,
  `lastLoginIp` varchar(64) DEFAULT NULL,
  `loginCount` int(11) DEFAULT '0' COMMENT '登录次数',
  `beginDate` datetime DEFAULT NULL COMMENT '帐号开始日期',
  `endDate` datetime DEFAULT NULL COMMENT '帐号结束日期',
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_sso_user_email` (`email`),
  KEY `index_sso_user_status` (`status`),
  KEY `index_sso_user_isdelete` (`isDelete`),
  KEY `index_sso_user_name` (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_user
-- ----------------------------
INSERT INTO `sso_user` VALUES ('1', 'Tree', '54a59a8ab309ec1a5d57b59b694fca33', '张三', '0', '1', '123456123333', '123456', 'tree@socsoft.net', '1', '2013-11-26 09:26:25', 'SOCRight', '180.168.5.182', '51', '2013-05-20 00:00:00', '2014-05-22 23:59:59', '', '2', 'Tree', '2012-07-09 21:32:06', 'Tree', '2013-06-03 15:38:50');

-- ----------------------------
-- Table structure for `sso_user_group`
-- ----------------------------
DROP TABLE IF EXISTS `sso_user_group`;
CREATE TABLE `sso_user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `status` int(11) DEFAULT NULL COMMENT '1可用，2不可用',
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_sso_user_group_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_user_group
-- ----------------------------
INSERT INTO `sso_user_group` VALUES ('1', '超级管理员组', '1', '', '2', 'Tree', '2012-07-10 04:38:48', 'Tree', '2012-07-10 04:38:48');

-- ----------------------------
-- Table structure for `sso_user_group_role`
-- ----------------------------
DROP TABLE IF EXISTS `sso_user_group_role`;
CREATE TABLE `sso_user_group_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userGroupID` int(11) DEFAULT NULL,
  `roleID` int(11) NOT NULL,
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_sso_user_group_role_usergroupid` (`userGroupID`),
  KEY `index_sso_user_group_role_roleid` (`roleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_user_group_role
-- ----------------------------
INSERT INTO `sso_user_group_role` VALUES ('1', '1', '1', '', '2', 'Tree', '2012-07-10 04:38:57', 'Tree', '2012-07-10 04:38:57');

-- ----------------------------
-- Table structure for `sso_user_group_user`
-- ----------------------------
DROP TABLE IF EXISTS `sso_user_group_user`;
CREATE TABLE `sso_user_group_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userGroupID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_sso_user_group_user_usergroupid` (`userGroupID`),
  KEY `index_sso_user_group_user_userid` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_user_group_user
-- ----------------------------
INSERT INTO `sso_user_group_user` VALUES ('1', '1', '1', '', '2', 'Tree', '2012-07-10 04:39:21', 'Tree', '2012-07-10 04:39:21');

-- ----------------------------
-- Table structure for `sso_user_role`
-- ----------------------------
DROP TABLE IF EXISTS `sso_user_role`;
CREATE TABLE `sso_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(11) DEFAULT NULL,
  `roleID` int(11) DEFAULT NULL,
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `isDelete` int(11) DEFAULT NULL COMMENT '是否删除，1删除，2不删除',
  `creater` varchar(32) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `lastUpdater` varchar(32) DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_sso_user_role_userid` (`userID`),
  KEY `index_sso_user_role_roleid` (`roleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_user_role
-- ----------------------------
INSERT INTO `sso_user_role` VALUES ('1', '1', '1', '', '2', 'Tree', '2012-07-12 15:39:09', 'Tree', '2012-07-12 15:39:09');
