#-*- encoding: utf-8 -*-


import tornado.web
import tornado.escape
import copy
from datetime import datetime, timedelta

import config

import admin_base_handler
from common import redis_cache, ssostatus, ssoerror
from helper import str_helper, http_helper
from logic import user_logic, role_logic, application_logic, usergroup_logic

class UserListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = ssostatus.operView
    def get(self):
        ps = self.get_page_config('用户列表')
        user = self.get_args(['id', 'realName', 'name', 'tel', 'mobile', 'email'], '')
        user['status'] = int(self.get_arg('status', '0'))
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = user_logic.UserLogic.instance().query_page(id = user['id'],
                    name = user['name'], realName = user['realName'], tel = user['tel'], mobile = user['mobile'], 
                    email = user['email'], status = user['status'], page = ps['page'], size = ps['size'])
        ps['user'] = user
        ps = self.format_none_to_empty(ps)
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/user/list.html', **ps)

class UserAddOrEditHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = 0
    def get(self):
        ps = self.get_page_config('创建用户')
        if ps['isedit']:
            self.check_oper_right(right = ssostatus.operEdit)
            ps['title'] = self.get_page_title('编辑用户')
            id = int(self.get_arg('id', '0'))
            user = user_logic.UserLogic.instance().query_one(id)
            if None == user:
                ps['msg'] = ssostatus.ResultInfo.get(103002, '')
                ps['gotoUrl'] = ps['siteDomain'] + 'Admin/User/List'
                user = {'id':'', 'name':'', 'realName':'', 'passWord':'','mobile':'','tel':'','email':'','status':1,'lastLoginTime':'','lastLoginApp':'','lastLoginIp':'','remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        else:
            self.check_oper_right(right = ssostatus.operAdd)
            user = self.get_args(['id', 'name', 'realName', 'passWord', 'mobile', 'tel', 'email', 'remark'], '')
            user['status'] = int(self.get_arg('status', '0'))
        ps['user'] = user
        print user
        ps = self.format_none_to_empty(ps)
        self.render('admin/user/add_or_edit.html', **ps)

    def post(self):
        ps = self.get_page_config('创建用户')
        if ps['isedit']:
            ps['title'] = self.get_page_title('编辑用户')

        user = self.get_args(['id', 'passWord', 'name', 'realName', 'mobile', 'tel', 'email', 'remark'], '')
        user['status'] = int(self.get_arg('status', '0'))        
        user['parentID'] = int(self.get_arg('parentID', '0'))
        ps['user'] = user
        msg = self.check_str_empty_input(user, ['name', 'realName', 'email', 'mobile'])
        if str_helper.is_null_or_empty(msg) == False:
            ps['msg'] = msg
            ps = self.format_none_to_empty(ps)
            self.render('admin/user/add_or_edit.html', **ps)
            return

        user['user'] = self.get_oper_user()
        ps['user'] = copy.copy(user)
        if ps['isedit']:
            self.check_oper_right(right = ssostatus.operEdit)
            try:
                info = user_logic.UserLogic.instance().update(id = user['id'], realName = user['realName'], 
                        parentID = user['parentID'], mobile = user['mobile'], tel = user['tel'], email = user['email'], 
                        status = user['status'], remark = user['remark'], user = user['user'])
                if info:
                    self.redirect(ps['siteDomain'] + 'Admin/User/List')
                    return
                else:
                    ps['msg'] = ssostatus.ResultInfo.get(101, '')
            except ssoerror.SsoError as e:
                ps['msg'] = e.msg
        else:
            self.check_oper_right(right = ssostatus.operEdit)            
            try:
                info = user_logic.UserLogic.instance().add(name = user['name'], passWord = user['passWord'], 
                            realName = user['realName'], mobile = user['mobile'], tel = user['tel'], email = user['email'],
                             status = user['status'], remark = user['remark'], parentID = user['parentID'], user = user['user'])
                if info > 0:
                    self.redirect(ps['siteDomain'] + 'Admin/User/List')
                    return
                else:
                    ps['msg'] = ssostatus.ResultInfo.get(101, '')
            except ssoerror.SsoError as e:
                ps['msg'] = e.msg
        ps = self.format_none_to_empty(ps)
        self.render('admin/user/add_or_edit.html', **ps)



class UserDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = ssostatus.operDel
    def post(self):
        id = int(self.get_arg('id', '0'))
        user = self.get_oper_user()
        type = user_logic.UserLogic.instance().delete(id = id, user = user)
        if type:
            self.out_ok()
        else:
            self.out_fail(code = 101)

class UserDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = ssostatus.operView
    def get(self):
        ps = self.get_page_config('用户详情')
        id = int(self.get_arg('id', '0'))
        user = user_logic.UserLogic.instance().query_one(id)
        if None == user:
            ps['msg'] = ssostatus.ResultInfo.get(103002, '')
            ps['gotoUrl'] = ps['siteDomain'] + 'Admin/User/List'
            user = {'id':'','name':'', 'passWord':'', 'statusname':'','mobile':'','tel':'','email':'','status':1,'lastLoginTime':'','lastLoginApp':'','lastLoginIp':'','remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}        
        ps['user'] = user
        ps = self.format_none_to_empty(ps)
        self.render('admin/user/detail.html', **ps)




class UserRoleListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager.UserBindRoleManager'
    _right = ssostatus.operView

    def get(self):
        ps = self.get_page_config('用户绑定角色列表')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = ssostatus.ResultInfo.get(105003, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/User/Add'
            self.render('admin/user/role_list.html', **ps)
            return
        
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = user_logic.UserLogic.instance().query_page_user_roles(
                userID = ps['userID'], page = ps['page'], size = ps['size'])
        user = user_logic.UserLogic.instance().query_one(id = ps['userID'])
        ps['userName'] = user['name']
        ps['userRealName'] = user['realName']
        ps = self.format_none_to_empty(ps)

        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/user/role_list.html', **ps)


class UserRoleBindHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager.UserBindRoleManager'
    _right = ssostatus.operEdit
    def get(self):
        ps = self.get_page_config('新增角色绑定用户')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = ssostatus.ResultInfo.get(103003, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/User/Add'
            self.render('admin/user/role_list.html', **ps)
            return

        ps['page'] = int(self.get_arg('page', '1'))        
        ps['roleName'] = self.get_arg('roleName', '')
        ps['roleID'] = int(self.get_arg('roleID', '0'))
        ps['roleInfo'] = ''
        if ps['roleID'] > 0:
            roleInfo = role_logic.RoleLogic.instance().query_one(id = ps['roleID'])
            ps['roleInfo'] = roleInfo['name']        

        ps['pagedata'] = role_logic.RoleLogic.instance().query_page(name = ps['roleName'], 
            status = ssostatus.statusActive, page = ps['page'], size = ps['size'])
        
        user = user_logic.UserLogic.instance().query_one(id = ps['userID'])
        ps['userInfo'] = user['name']
        ps['userRealName'] = user['realName']

        ps = self.format_none_to_empty(ps)
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/user/role_bind.html', **ps)


    def post(self):
        userID = int(self.get_arg('userID', '0'))
        roleID = int(self.get_arg('roleID', '0'))
        if userID <= 0 or roleID <= 0:
            self.out_fail(code = 103004)
            return
        id = user_logic.UserLogic.instance().bind_user_role(userID = userID, roleID = roleID, user = self.get_oper_user())
        if None != id and id > 0:
            self.out_ok()
        else:
            self.out_fail(code = 103005)


class UserRoleDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager.UserBindRoleManager'
    _right = ssostatus.operDel

    def post(self):
        id = int(self.get_arg('id', '0'))
        if id <= 0:
            self.out_fail(code = 103006)
            return
        type = user_logic.UserLogic.instance().del_user_role(id = id, user = self.get_oper_user())
        if type:
            self.out_ok()
        else:
            self.out_fail(code = 103006)


class UserRightDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager.UserBindRoleManager'
    _right = ssostatus.operView
    def get(self):
        ps = self.get_page_config('用户应用权限信息')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = ssostatus.ResultInfo.get(103007, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/User/List'
            self.render('admin/user/right.html', **ps)
            return
        
        ps['appCode'] = self.get_arg('appCode', '')
        ps['apps'] = application_logic.ApplicationLogic.instance().query_all_by_active()
        if None == ps['apps'] or len(ps['apps']) <= 0:
            ps['msg'] = ssostatus.ResultInfo.get(101004, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/Application/Add'
            self.render('admin/user/right_detail.html', **ps)
            return
        else:
            if '' == ps['appCode']:
                ps['appCode'] = ps['apps'][0]['code']
        
        ps['roles'] = user_logic.UserLogic.instance().query_all_user_roles(
                userID = ps['userID'])
        user = user_logic.UserLogic.instance().query_one(id = ps['userID'])
        ps['userName'] = user['name']
        ps['userRealName'] = user['realName']
        ps['userGroups'] = usergroup_logic.UserGroupLogic.instance().query_all_user_groups(
                userID = ps['userID'])
        
        ps = self.format_none_to_empty(ps)
        funcs = user_logic.UserLogic.instance().query_user_app_right(userID = ps['userID'], appCode = ps['appCode'])
        ps['funcs'] = funcs
        
        self.render('admin/user/right_detail.html', **ps)


class UserUserGroupListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindUserManager'
    _right = ssostatus.operView

    def get(self):
        ps = self.get_page_config('用户绑定用户组列表')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = ssostatus.ResultInfo.get(103007, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/User/List'
            self.render('admin/user/right.html', **ps)
            return
        
        user = user_logic.UserLogic.instance().query_one(id = ps['userID'])
        ps['userName'] = user['name']
        ps['userRealName'] = user['realName']

        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = usergroup_logic.UserGroupLogic.instance().query_page_user_groups(
                userID = ps['userID'], page = ps['page'], size = ps['size'])        
        ps = self.format_none_to_empty(ps)
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])
        self.render('admin/user/group_list.html', **ps)