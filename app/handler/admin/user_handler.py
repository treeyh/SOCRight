#-*- encoding: utf-8 -*-


import tornado.web
import tornado.escape
import copy
from datetime import datetime, timedelta

import config

import admin_base_handler
from common import redis_cache, state, error
from helper import str_helper, http_helper
from logic import user_logic, role_logic, application_logic, usergroup_logic, department_logic

class UserListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operView
    def get(self):
        ps = self.get_page_config('用户列表')
        user = self.get_args(['id', 'realName', 'name', 'tel', 'mobile', 'email'], '')
        user['status'] = int(self.get_arg('status', '0'))
        user['departmentID'] = int(self.get_arg('departmentID', '0'))
        ps['deps'] = department_logic.DepartmentLogic.instance().query_all_by_active()
        ps['page'] = int(self.get_arg('page', '1'))
        ps['userStatus'] = state.UserStatus
        ps['pagedata'] = user_logic.UserLogic.instance().query_page(id = user['id'],
                    name = user['name'], realName = user['realName'], departmentID = user['departmentID'],
                     tel = user['tel'], mobile = user['mobile'], email = user['email'], 
                     status = user['status'], page = ps['page'], size = ps['size'])
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
            self.check_oper_right(right = state.operEdit)
            ps['title'] = self.get_page_title('编辑用户')
            id = int(self.get_arg('id', '0'))
            user = user_logic.UserLogic.instance().query_one(id)
            if None == user:
                ps['msg'] = state.ResultInfo.get(103002, '')
                ps['gotoUrl'] = ps['siteDomain'] + 'Admin/User/List'
                user = {'id':'', 'name':'', 'departmentID': '', 'realName':'','beginDate':'','endDate':'', 'passWord':'','mobile':'','tel':'','email':'','status':1,'lastLoginTime':'','lastLoginApp':'','lastLoginIp':'','remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        else:
            self.check_oper_right(right = state.operAdd)
            user = self.get_args(['id', 'name', 'realName', 'departmentID', 'passWord', 'mobile', 'tel', 'email', 'remark'], '')
            user['beginDate'] = str_helper.get_now_datestr()
            user['endDate'] = str_helper.get_add_datest(days = 365)
            user['status'] = int(self.get_arg('status', '0'))
        ps['user'] = user
        ps['userStatus'] = state.UserStatus
        ps['deps'] = department_logic.DepartmentLogic.instance().query_all_by_active()

        ps = self.format_none_to_empty(ps)
        self.render('admin/user/add_or_edit.html', **ps)

    def post(self):
        ps = self.get_page_config('创建用户')
        if ps['isedit']:
            ps['title'] = self.get_page_title('编辑用户')

        user = self.get_args(['id', 'passWord', 'name', 'realName', 'mobile', 'tel', 'email', 'remark', 'beginDate', 'endDate'], '')
        user['status'] = int(self.get_arg('status', '0'))
        user['departmentID'] = int(self.get_arg('departmentID', '0'))
        user['parentID'] = int(self.get_arg('parentID', '0'))
        ps['user'] = user
        ps['userStatus'] = state.UserStatus
        ps['deps'] = department_logic.DepartmentLogic.instance().query_all_by_active()
        msg = self.check_str_empty_input(user, ['name', 'realName', 'email', 'mobile', 'beginDate', 'endDate'])
        if str_helper.is_null_or_empty(msg) == False:
            ps['msg'] = msg
            ps = self.format_none_to_empty(ps)
            self.render('admin/user/add_or_edit.html', **ps)
            return

        user['user'] = self.get_oper_user()
        ps['user'] = copy.copy(user)
        if ps['isedit']:
            self.check_oper_right(right = state.operEdit)
            try:
                info = user_logic.UserLogic.instance().update(id = user['id'], realName = user['realName'], 
                        departmentID = user['departmentID'], parentID = user['parentID'], mobile = user['mobile'], 
                        tel = user['tel'], email = user['email'], status = user['status'], beginDate = user['beginDate'], 
                        endDate = user['endDate'], remark = user['remark'], user = user['user'])
                if info:
                    ps = self.get_ok_and_back_params(ps = ps)
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        else:
            self.check_oper_right(right = state.operEdit)            
            try:
                info = user_logic.UserLogic.instance().add(name = user['name'], passWord = user['passWord'], 
                            realName = user['realName'], departmentID = user['departmentID'], mobile = user['mobile'], 
                            tel = user['tel'], email = user['email'],beginDate = user['beginDate'], 
                            endDate = user['endDate'], status = user['status'], remark = user['remark'], 
                            parentID = user['parentID'], user = user['user'])
                if info > 0:
                    ps = self.get_ok_and_back_params(ps = ps)
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        ps = self.format_none_to_empty(ps)
        self.render('admin/user/add_or_edit.html', **ps)



class UserDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operDel
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
    _right = state.operView
    def get(self):
        ps = self.get_page_config('用户详情')
        id = int(self.get_arg('id', '0'))
        user = user_logic.UserLogic.instance().query_one(id)
        if None == user:
            ps['msg'] = state.ResultInfo.get(103002, '')
            ps['gotoUrl'] = ps['siteDomain'] + 'Admin/User/List'
            user = {'id':'','name':'', 'passWord':'', 'statusname':'','mobile':'','tel':'','email':'','status':1,'lastLoginTime':'','lastLoginApp':'','lastLoginIp':'','remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}        
        ps['user'] = user
        ps = self.format_none_to_empty(ps)
        self.render('admin/user/detail.html', **ps)




class UserRoleListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager.UserBindRoleManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config('用户绑定角色列表')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = state.ResultInfo.get(105003, '')
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
    _right = state.operEdit
    def get(self):
        ps = self.get_page_config('新增角色绑定用户')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = state.ResultInfo.get(103003, '')
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
            status = state.statusActive, page = ps['page'], size = ps['size'])
        
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
    _right = state.operDel

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
    _right = state.operView
    def get(self):
        ps = self.get_page_config('用户应用权限信息')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = state.ResultInfo.get(103007, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/User/List'
            self.render('admin/user/right.html', **ps)
            return
        
        ps['appCode'] = self.get_arg('appCode', '')
        ps['apps'] = application_logic.ApplicationLogic.instance().query_all_by_active()
        if None == ps['apps'] or len(ps['apps']) <= 0:
            ps['msg'] = state.ResultInfo.get(101004, '')
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
    _right = state.operView

    def get(self):
        ps = self.get_page_config('用户绑定用户组列表')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = state.ResultInfo.get(103007, '')
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


class UserResetPassWordHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindUserManager'
    _right = state.operView

    def post(self):
        # ps = self.get_page_config('重置用户密码')
        name = self.get_arg('name', '')
        # userName = self.get_arg('userName', '')
        print 'name:' + name
        if None == name or '' == name:
            self.out_fail(code = 103007)
            return
        
        newPW = user_logic.UserLogic.instance().reset_password(name)
        if None == newPW or '' == newPW:
            self.out_fail(code = 101)
            return
        self.out_ok(data = '{"newpw":"'+newPW+'"}')


#导出用户excel
class UserExportHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operView
    def get(self):
        import sys
        reload(sys)                        
        sys.setdefaultencoding('utf-8')    
        ps = self.get_page_config('导出用户Excel')
        user = self.get_args(['id', 'realName', 'name', 'tel', 'mobile', 'email'], '')
        user['status'] = int(self.get_arg('status', '0'))
        user['departmentID'] = int(self.get_arg('departmentID', '0'))
        ps['deps'] = department_logic.DepartmentLogic.instance().query_all_by_active()
        ps['page'] = int(self.get_arg('page', '1'))
        ps['userStatus'] = state.UserStatus
        ps['pagedata'] = user_logic.UserLogic.instance().query_page(id = user['id'],
                    name = user['name'], realName = user['realName'], departmentID = user['departmentID'],
                     tel = user['tel'], mobile = user['mobile'], email = user['email'], 
                     status = user['status'], page = ps['page'], size = 999)

        users = ps['pagedata']['data']

        #生成excel文件
        info = u'''<table><tr><td>用户ID</td><td>用户名</td><td>姓名</td><td>部门</td><td>状态</td>
                    <td>最后登录时间</td><td>创建人</td><td>创建时间</td><td>最后更新人</td><td>最后更新时间</td></tr>'''

        for user in users:
            u = u'''<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>''' % (str(user['id']), user['name'], user['realName'], 
                        user['departmentName'], user['statusname'], user['lastLoginTime'], user['creater'], str(user['createTime'])[0:-3], 
                        user['lastUpdater'], str(user['lastUpdateTime'])[0:-3] )
            info = info + u
        info = info + u'</table>'
        fileName = config.SOCRightConfig['exportUserPath'] + str_helper.get_now_datestr() +'_'+ str_helper.get_uuid() + '.xls'

        path = config.SOCRightConfig['realPath'] + fileName
        file_object = open(path, 'w')
        file_object.write(info)
        file_object.close( )    
        self.redirect(config.SOCRightConfig['siteDomain']+fileName)




        