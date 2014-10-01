/*
Navicat MySQL Data Transfer

Source Server         : 192.168.18.188
Source Server Version : 50167
Source Host           : 192.168.18.188:3306
Source Database       : soc_sso_right

Target Server Type    : MYSQL
Target Server Version : 50167
File Encoding         : 65001

Date: 2014-10-01 15:07:43
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
INSERT INTO `sso_application` VALUES ('SOCProject', '123', '123', '123', '1', '123', '2', 'Tree', '2014-04-23 09:50:22', 'Tree', '2014-04-23 09:50:22');
INSERT INTO `sso_application` VALUES ('SOCRight', 'SOC权限管理系统', 'Tree', 'http://ssoadmin.ejyi.com/Admin/Main', '1', '1234', '2', 'Tree', '2012-06-20 10:15:43', 'Tree', '2013-09-05 10:02:32');

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_department
-- ----------------------------
INSERT INTO `sso_department` VALUES ('1', '技术研发部', '1', '11', '2', 'Tree', '2013-05-15 15:48:22', 'Tree', '2013-05-21 17:29:15');

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
  `rights` varchar(1024) DEFAULT NULL COMMENT '功能权限',
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
) ENGINE=InnoDB AUTO_INCREMENT=195 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_func
-- ----------------------------
INSERT INTO `sso_func` VALUES ('9', 'SOCRight', '应用管理', 'AppManager', '0', 'SOCRight.AppManager', '1:浏览;2:新增;4:编辑;8:删除', '', '1', '1', '', '2', 'Tree', '2012-07-09 10:14:03', 'Tree', '2012-07-09 10:14:03');
INSERT INTO `sso_func` VALUES ('10', 'SOCRight', '功能管理', 'FuncManager', '0', 'SOCRight.FuncManager', '1:浏览;2:新增;4:编辑;8:删除', '', '1', '1', '', '2', 'Tree', '2012-07-09 10:14:35', 'Tree', '2013-09-26 18:26:40');
INSERT INTO `sso_func` VALUES ('11', 'SOCRight', '用户管理', 'UserManager', '0', 'SOCRight.UserManager', '1:浏览;2:新增;4:编辑;8:删除', '[{\"k\":\"Export\",\"v\":\"导出用户数据\"},{\"k\":\"ResetPassword\",\"v\":\"重置用户密码\"},{\"k\":\"Lock\",\"v\":\"锁定用户\"}]', '8', '1', '', '2', 'Tree', '2012-07-09 10:14:58', 'Tree', '2014-04-22 15:12:14');
INSERT INTO `sso_func` VALUES ('12', 'SOCRight', '用户组管理', 'UserGroupManager', '0', 'SOCRight.UserGroupManager', '1:浏览;2:新增;4:编辑;8:删除', '', '7', '1', '', '2', 'Tree', '2012-07-09 10:15:26', 'Tree', '2014-04-22 15:12:57');
INSERT INTO `sso_func` VALUES ('13', 'SOCRight', '角色管理', 'RoleManager', '0', 'SOCRight.RoleManager', '1:浏览;2:新增;4:编辑;8:删除', '', '6', '1', '', '2', 'Tree', '2012-07-09 10:15:51', 'Tree', '2014-04-22 15:13:02');
INSERT INTO `sso_func` VALUES ('14', 'SOCRight', '用户绑定角色管理', 'UserBindRoleManager', '11', 'SOCRight.UserManager.UserBindRoleManager', '1:浏览;2:新增;4:编辑;8:删除', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:17:52', 'Tree', '2012-07-09 10:17:52');
INSERT INTO `sso_func` VALUES ('15', 'SOCRight', '用户组绑定角色管理', 'UserGroupBindRoleManager', '12', 'SOCRight.UserGroupManager.UserGroupBindRoleManager', '1:浏览;2:新增;4:编辑;8:删除', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:25:39', 'Tree', '2012-07-09 10:25:39');
INSERT INTO `sso_func` VALUES ('16', 'SOCRight', '用户组绑定用户管理', 'UserGroupBindUserManager', '12', 'SOCRight.UserGroupManager.UserGroupBindUserManager', '1:浏览;2:新增;4:编辑;8:删除', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:27:58', 'Tree', '2012-07-09 10:27:58');
INSERT INTO `sso_func` VALUES ('17', 'SOCRight', '角色绑定权限管理', 'RoleBindRightManager', '13', 'SOCRight.RoleManager.RoleBindRightManager', '1:浏览;2:新增;4:编辑;8:删除', '', '0', '1', '', '2', 'Tree', '2012-07-09 10:39:13', 'Tree', '2012-07-09 10:39:13');
INSERT INTO `sso_func` VALUES ('18', 'SOCRight', '登录操作', 'Login', '0', 'SOCRight.Login', '1:登录', '[{\"k\":\"a1\",\"v\":\"xxx功能\"},{\"k\":\"a2\",\"v\":\"yyy功能\"}]', '15', '1', '', '2', 'Tree', '2012-07-10 04:00:12', 'Tree', '2014-10-01 14:07:19');
INSERT INTO `sso_func` VALUES ('190', 'SOCRight', '部门管理', 'DepartmentManager', '0', 'SOCRight.DepartmentManager', '1:浏览;2:新增;4:编辑;8:删除', '', '10', '1', '', '2', 'Tree', '2013-07-22 14:48:26', 'Tree', '2014-04-22 15:11:09');
INSERT INTO `sso_func` VALUES ('192', 'SOCRight', '操作日志管理', 'OperLogManager', '0', 'SOCRight.OperLogManager', '1:浏览;2:新增;4:编辑;8:删除', '[{\"k\":\"Export\",\"v\":\"导出操作数据\"}]', '0', '1', '', '2', 'Tree', '2013-08-26 14:50:01', 'Tree', '2014-04-22 15:13:18');
INSERT INTO `sso_func` VALUES ('193', 'SOCRight', '云海权限系统管理', 'SOCRight', '9', 'SOCRight.AppManager.SOCRight', '1:浏览;2:新增;4:编辑;8:删除', '', '1', '1', '', '2', 'Tree', '2014-04-22 15:08:42', 'Tree', '2014-04-22 15:10:52');
INSERT INTO `sso_func` VALUES ('194', 'SOCRight', '123管理', 'SOCProject', '9', 'SOCRight.AppManager.SOCProject', '1:浏览;2:新增;4:编辑;8:删除', '', '0', '1', '', '2', 'Tree', '2014-04-23 09:50:22', 'Tree', '2014-04-23 09:50:22');

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
) ENGINE=InnoDB AUTO_INCREMENT=246 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_role
-- ----------------------------
INSERT INTO `sso_role` VALUES ('1', '超级管理员', '1', '', '2', 'Tree', '2012-07-10 03:56:13', 'Tree', '2012-07-10 03:56:13');
INSERT INTO `sso_role` VALUES ('2', '测试角色', '1', '', '2', 'Tree', '2014-04-23 10:50:25', 'Tree', '2014-04-23 10:50:25');

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
) ENGINE=InnoDB AUTO_INCREMENT=1759 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_role_right
-- ----------------------------
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
  `lockTime` datetime DEFAULT NULL COMMENT '锁定时间',
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_user
-- ----------------------------
INSERT INTO `sso_user` VALUES ('1', 'Tree', '54a59a8ab309ec1a5d57b59b694fca33', '余海', '0', '1', '123456123333', '123456', 'treeyh@126.com', '1', '2014-10-01 10:44:24', 'SOCRight', '192.168.18.177', '74', '2013-05-20 00:00:00', '2040-05-22 23:59:59', '', null, '2', 'Tree', '2012-07-09 21:32:06', 'Tree', '2013-06-03 15:38:50');
INSERT INTO `sso_user` VALUES ('2', '测试', '54a59a8ab309ec1a5d57b59b694fca33', '测试', '0', null, '123', '', 'yuhai717@163.com', '1', null, null, null, '0', '2013-05-20 00:00:00', '2014-05-20 00:00:00', '', null, '1', 'Tree', '2012-07-10 21:32:06', 'Tree', '2013-04-27 14:00:00');
INSERT INTO `sso_user` VALUES ('5', 'Prince', '85eab839754dcbe976cbedcc8b805f6d', '常博', '0', null, '15000274561', '', 'changbo@tv189.com', '1', '2013-04-27 13:49:42', 'AMSManager', '192.168.99.66', '0', '2013-05-20 00:00:00', '2013-06-20 00:00:00', '', null, '1', 'Tree', '2012-07-24 13:21:47', 'Tree', '2014-04-23 10:50:04');
INSERT INTO `sso_user` VALUES ('6', 'test', 'f98b86f187c10f0d937cf55ce2ab9e41', 'test', '0', '1', 'test', 'test', 'test@163.com', '1', '2014-04-23 10:43:21', 'SOCRight', '192.168.18.169', '4', '2014-04-15 00:00:00', '2015-04-23 23:59:59', '', null, '2', 'Tree', '2014-04-23 10:35:00', 'Tree', '2014-04-23 10:35:00');

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_user_group_user
-- ----------------------------
INSERT INTO `sso_user_group_user` VALUES ('1', '1', '1', '', '2', 'Tree', '2012-07-10 04:39:21', 'Tree', '2012-07-10 04:39:21');
INSERT INTO `sso_user_group_user` VALUES ('2', '1', '5', '', '2', 'Tree', '2012-07-24 13:23:04', 'Tree', '2012-07-24 13:23:04');

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sso_user_role
-- ----------------------------
INSERT INTO `sso_user_role` VALUES ('1', '1', '1', '', '2', 'Tree', '2012-07-12 15:39:09', 'Tree', '2012-07-12 15:39:09');
INSERT INTO `sso_user_role` VALUES ('2', '5', '1', '', '1', 'Tree', '2012-07-24 13:22:24', 'Tree', '2013-09-16 09:45:47');
