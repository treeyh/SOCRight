#-*- encoding: utf-8 -*-


import tornado.web
import tornado.escape
import config

from datetime import datetime, timedelta
import admin_base_handler
from common import redis_cache, state, error
from helper import str_helper, http_helper
from logic import usergroup_logic, user_logic, role_logic, application_logic

class UserGroupListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '用户组列表')
        userGroup = self.get_args(['id', 'name'], '')
        userGroup['status'] = int(self.get_arg('status', '0'))
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = usergroup_logic.query_page(id = userGroup['id'], 
                    name = userGroup['name'], status = userGroup['status'], page = ps['page'], size = ps['size'])
        ps['userGroup'] = userGroup
        ps = self.format_none_to_empty(ps)
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/usergroup/list.html', **ps)

class UserGroupAddOrEditHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager'
    _right = 0
    def get(self):
        ps = self.get_page_config(title = '创建用户组', refUrl = config.SOCRightConfig['siteDomain'] + 'Admin/UserGroup/List')
        if ps['isedit']:
            ps['title'] = self.get_page_title('编辑用户组')
            id = int(self.get_arg('id', '0'))
            usergroup = usergroup_logic.query_one(id)
            if None == usergroup:
                ps['msg'] = state.ResultInfo.get(105002, '')                
                role = {'id':'','name':'','status':1,'remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        else:
            usergroup = self.get_args(['id', 'name', 'remark'], '')
            usergroup['status'] = int(self.get_arg('status', '0'))
        ps['usergroup'] = usergroup
        ps = self.format_none_to_empty(ps)
        self.render('admin/usergroup/add_or_edit.html', **ps)

    def post(self):
        ps = self.get_page_config(title = '创建用户组')
        if ps['isedit']:
            ps['title'] = self.get_page_title('编辑用户组')
        
        usergroup = self.get_args(['id', 'name', 'remark'], '')
        usergroup['status'] = int(self.get_arg('status', '0'))
        msg = self.check_str_empty_input(usergroup, ['name'])
        ps['usergroup'] = usergroup
        if str_helper.is_null_or_empty(msg) == False:
            ps['msg'] = msg
            ps = self.format_none_to_empty(ps)
            self.render('admin/usergroup/add_or_edit.html', **ps)
            return
        usergroup['user'] = self.get_oper_user()
        
        if ps['isedit']:
            try:
                og = usergroup_logic.query_one(usergroup['id'])
                info = usergroup_logic.update(id = usergroup['id'], name = usergroup['name'], 
                    status = usergroup['status'], remark = usergroup['remark'], user = usergroup['user'])
                if info:
                    ng = usergroup_logic.query_one(usergroup['id'])
                    self.write_oper_log(action = 'userGroupEdit', targetType = 6, targetID = str(ng['id']), targetName = ng['name'], startStatus = str_helper.json_encode(og), endStatus= str_helper.json_encode(ng))
                    ps = self.get_ok_and_back_params(ps = ps, refUrl = ps['refUrl'])
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        else:
            try:
                info = usergroup_logic.add(name = usergroup['name'], 
                    status = usergroup['status'], remark = usergroup['remark'], user = usergroup['user'])
                if info > 0:
                    ng = usergroup_logic.query_one_by_name(usergroup['name'])
                    self.write_oper_log(action = 'userGroupCreate', targetType = 6, targetID = str(ng['id']), targetName = ng['name'], startStatus = '', endStatus= str_helper.json_encode(ng))
                    ps = self.get_ok_and_back_params(ps = ps, refUrl = ps['refUrl'])
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        ps = self.format_none_to_empty(ps)
        self.render('admin/usergroup/add_or_edit.html', **ps)



class UserGroupDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager'
    _right = state.operDel

    def post(self):
        id = int(self.get_arg('id', '0'))
        user = self.get_oper_user()
        og = usergroup_logic.query_one(id)
        type = usergroup_logic.delete(id = id, user = user)
        if type:
            self.write_oper_log(action = 'userGroupDelete', targetType = 6, targetID = str(og['id']), targetName = og['name'], startStatus = str_helper.json_encode(og), endStatus= '')
            self.out_ok()
        else:
            self.out_fail(code = 101)

class UserGroupDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager'
    _right = state.operView
    def get(self):
        ps = self.get_page_config(title = '用户组详情')
        id = int(self.get_arg('id', '0'))
        usergroup = usergroup_logic.query_one(id)
        if None == usergroup:
            ps['msg'] = state.ResultInfo.get(105002, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/UserGroup/List'
            usergroup = {'id':'','name':'', 'statusname':'','status':1, 'remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}        
        ps['usergroup'] = usergroup
        ps = self.format_none_to_empty(ps)
        self.render('admin/usergroup/detail.html', **ps)



class UserGroupUserListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindUserManager'
    _right = state.operView
    def get(self):
        ps = self.get_page_config(title = '用户组绑定用户列表')
        ps['userGroupID'] = int(self.get_arg('id', '0'))
        userGroups = usergroup_logic.query_all_by_active()
        if None == userGroups or len(userGroups) == 0:
            ps['msg'] = state.ResultInfo.get(105003, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/UserGroup/Add'
            self.render('admin/usergroup/user_list.html', **ps)
            return
        else:
            if 0 == ps['userGroupID']:
                ps['userGroupID'] = userGroups[0]['id']
        
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = usergroup_logic.query_page_group_users(
                userGroupID = ps['userGroupID'], page = ps['page'], size = ps['size'])
    
        ps['userGroups'] = userGroups
        ps = self.format_none_to_empty(ps)
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/usergroup/user_list.html', **ps)


class UserGroupUserBindHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindUserManager'
    _right = state.operEdit

    def get(self):
        ps = self.get_page_config(title = '新增用户绑定用户组')
        ps['userGroupID'] = int(self.get_arg('userGroupID', '0'))
        userGroups = usergroup_logic.query_all_by_active()
        if None == userGroups or len(userGroups) == 0:
            ps['msg'] = state.ResultInfo.get(105003, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/UserGroup/Add'
            self.render('admin/usergroup/user_bind.html', **ps)
            return
        else:
            if 0 == ps['userGroupID']:
                ps['userGroupID'] = userGroups[0]['id']

        ps['userGroups'] = userGroups
        ps['page'] = int(self.get_arg('page', '1'))        
        ps['userName'] = self.get_arg('userName', '')
        ps['userID'] = int(self.get_arg('userID', '0'))
        ps['userInfo'] = ''
        if ps['userID'] > 0:
            userInfo = user_logic.query_one(id = ps['userID'])
            ps['userInfo'] = userInfo['name']        

        ps['pagedata'] = user_logic.query_page(name = ps['userName'], 
            status = state.statusActive, page = ps['page'], size = ps['size'])
        ps = self.format_none_to_empty(ps)
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/usergroup/user_bind.html', **ps)


    def post(self):
        userGroupID = int(self.get_arg('userGroupID', '0'))
        userID = int(self.get_arg('userID', '0'))
        if userGroupID <= 0 or userID <= 0:
            self.out_fail(code = 105004)
            return
        id = usergroup_logic.bind_group_user(userGroupID = userGroupID, userID = userID, user = self.get_oper_user())
        if None != id and id > 0:
            self.write_oper_log(action = 'userGroupBindUser', targetType = 6, targetID = str(userGroupID), targetName = str(userID), startStatus = str(userGroupID), endStatus= str(userID))
            self.out_ok()
        else:
            self.out_fail(code = 105005)


class UserGroupUserDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindUserManager'
    _right = state.operDel
    def post(self):
        id = int(self.get_arg('id', '0'))
        userGroupID = int(self.get_arg('userGroupID', '0'))
        if id <= 0 or userGroupID <= 0:
            self.out_fail(code = 105006)
            return
        oug = usergroup_logic.get_group_user(id = id)
        type = usergroup_logic.del_group_user(id = id, userGroupID = userGroupID, user = self.get_oper_user())
        if type:
            self.write_oper_log(action = 'userGroupDeleteUser', targetType = 6, targetID = str(id), targetName = '', startStatus = str(oug['userGroupID']), endStatus= str(oug['userID']))
            self.out_ok()
        else:
            self.out_fail(code = 105006)



class UserGroupRoleListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindRoleManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '用户组绑定角色列表')
        ps['userGroupID'] = int(self.get_arg('id', '0'))
        userGroups = usergroup_logic.query_all_by_active()
        if None == userGroups or len(userGroups) == 0:
            ps['msg'] = state.ResultInfo.get(105003, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/UserGroup/Add'
            self.render('admin/usergroup/role_list.html', **ps)
            return
        else:
            if 0 == ps['userGroupID']:
                ps['userGroupID'] = userGroups[0]['id']
        
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = usergroup_logic.query_page_group_roles(
                userGroupID = ps['userGroupID'], page = ps['page'], size = ps['size'])
        ps = self.format_none_to_empty(ps)
        ps['userGroups'] = userGroups
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/usergroup/role_list.html', **ps)


class UserGroupRoleBindHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindRoleManager'
    _right = state.operEdit

    def get(self):
        ps = self.get_page_config(title = '新增角色绑定用户组')
        ps['userGroupID'] = int(self.get_arg('userGroupID', '0'))
        userGroups = usergroup_logic.query_all_by_active()
        if None == userGroups or len(userGroups) == 0:
            ps['msg'] = state.ResultInfo.get(105003, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/UserGroup/Add'
            self.render('admin/usergroup/user_bind.html', **ps)
            return
        else:
            if 0 == ps['userGroupID']:
                ps['userGroupID'] = userGroups[0]['id']

        ps['userGroups'] = userGroups
        ps['page'] = int(self.get_arg('page', '1'))        
        ps['roleName'] = self.get_arg('roleName', '')
        ps['roleID'] = int(self.get_arg('roleID', '0'))
        ps['roleInfo'] = ''
        if ps['roleID'] > 0:
            roleInfo = role_logic.query_one(id = ps['roleID'])
            ps['roleInfo'] = roleInfo['name']        

        ps['pagedata'] = role_logic.query_page(name = ps['roleName'], 
            status = state.statusActive, page = ps['page'], size = ps['size'])
        ps = self.format_none_to_empty(ps)
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/usergroup/role_bind.html', **ps)


    def post(self):
        userGroupID = int(self.get_arg('userGroupID', '0'))
        roleID = int(self.get_arg('roleID', '0'))
        if userGroupID <= 0 or roleID <= 0:
            self.out_fail(code = 105007)
            return
        id = usergroup_logic.bind_group_role(userGroupID = userGroupID, roleID = roleID, user = self.get_oper_user())
        if None != id and id >= 0:
            self.write_oper_log(action = 'userGroupBindRole', targetType = 6, targetID = str(id), targetName = '', startStatus = str(userGroupID), endStatus= str(roleID))
            self.out_ok()
        else:
            self.out_fail(code = 105008)


class UserGroupRoleDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindRoleManager'
    _right = state.operDel

    def post(self):
        id = int(self.get_arg('id', '0'))
        userGroupID = int(self.get_arg('userGroupID', '0'))
        if id <= 0 or userGroupID <= 0:
            self.out_fail(code = 105009)
            return
        ogr = usergroup_logic.get_group_role(id = id)
        type = usergroup_logic.del_group_role(id = id, userGroupID = userGroupID, user = self.get_oper_user())
        if type:
            self.write_oper_log(action = 'userGroupDeleteRole', targetType = 6, targetID = str(id), targetName = '', startStatus = str(ogr['userGroupID']), endStatus= str(ogr['roleID']))
            self.out_ok()
        else:
            self.out_fail(code = 105009)


class UserGroupRightDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindRoleManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '用户组应用权限信息')
        ps['userGroupID'] = int(self.get_arg('id', '0'))
        if 0 == ps['userGroupID']:
            ps['msg'] = state.ResultInfo.get(105010, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/UserGroup/List'
            self.render('admin/usergroup/right_detail.html', **ps)
            return

        ps['appCode'] = self.get_arg('appCode', '')
        ps['apps'] = application_logic.query_all_by_active()
        if None == ps['apps'] or len(ps['apps']) <= 0:
            ps['msg'] = state.ResultInfo.get(101004, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/Application/Add'
            self.render('admin/usergroup/right_detail.html', **ps)
            return
        else:
            if '' == ps['appCode']:
                ps['appCode'] = ps['apps'][0]['code']

        userGroup = usergroup_logic.query_one(ps['userGroupID'])
        ps['userGroupName'] = userGroup['name'] if None != userGroup else ''
        
        ps['roles'] = usergroup_logic.query_all_group_roles(userGroupID = ps['userGroupID'])
        
        ps = self.format_none_to_empty(ps)
        funcs = usergroup_logic.query_user_group_app_right(userGroupID = ps['userGroupID'], appCode = ps['appCode'])
        ps['funcs'] = funcs
        
        self.render('admin/usergroup/right_detail.html', **ps)