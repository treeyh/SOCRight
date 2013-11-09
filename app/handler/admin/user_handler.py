#-*- encoding: utf-8 -*-


import tornado.web
import tornado.escape
import copy
from datetime import datetime, timedelta

import config

import admin_base_handler
from common import redis_cache, state, error
from helper import str_helper, http_helper
from logic import user_logic, role_logic, application_logic, usergroup_logic, department_logic, oper_log_logic

class UserListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operView
    def get(self):
        ps = self.get_page_config(title = '用户列表')
        
        ps['ExportType'] = self.check_oper_right_custom_right(self._rightKey, self._exportUserKey)
        ps['LockType'] = self.check_oper_right_custom_right(self._rightKey, self._lockUserKey)
        user = self.get_args(['id', 'realName', 'name', 'tel', 'mobile', 'email', 'createTimeBegin', 'createTimeEnd', 'lastUpdateTimeBegin', 'lastUpdateTimeEnd'], '')
        user['status'] = int(self.get_arg('status', '0'))
        user['departmentID'] = int(self.get_arg('departmentID', '0'))
        ps['deps'] = department_logic.query_all_by_active()
        ps['page'] = int(self.get_arg('page', '1'))
        ps['userStatus'] = state.UserStatus
        ps['pagedata'] = user_logic.query_page(id = user['id'],
                    name = user['name'], realName = user['realName'], departmentID = user['departmentID'],
                     tel = user['tel'], mobile = user['mobile'], email = user['email'], 
                     status = user['status'], createTimeBegin = user['createTimeBegin'], createTimeEnd = user['createTimeEnd'], lastUpdateTimeBegin = user['lastUpdateTimeBegin'], lastUpdateTimeEnd = user['lastUpdateTimeEnd'], page = ps['page'], size = ps['size'])
        ps['user'] = user
        ps = self.format_none_to_empty(ps)
        ps['pager'] = self.build_page_html_bs(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])
        self.render('admin/user/list_bs.html', **ps)


class UserAddOrEditHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = 0
    def get(self):
        ps = self.get_page_config(title = '创建用户', refUrl = config.SOCRightConfig['siteDomain'] + 'Admin/User/List')

        ps['ResetPasswordType'] = self.check_oper_right_custom_right(self._rightKey, self._resetPwKey)
        if ps['isedit']:
            self.check_oper_right(right = state.operEdit)
            ps['title'] = self.get_page_title('编辑用户')
            id = int(self.get_arg('id', '0'))
            user = user_logic.query_one(id)
            if None == user:
                ps['msg'] = state.ResultInfo.get(103002, '')
                user = {'id':'', 'name':'', 'departmentID': '', 'realName':'','beginDate':'','endDate':'', 'passWord':'','mobile':'','tel':'','email':'','status':1,'lastLoginTime':'','lastLoginApp':'','lastLoginIp':'','remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        else:
            self.check_oper_right(right = state.operAdd)
            user = self.get_args(['id', 'name', 'realName', 'departmentID', 'passWord', 'mobile', 'tel', 'email', 'remark'], '')
            user['beginDate'] = str_helper.get_now_datestr()
            user['endDate'] = str_helper.get_add_datest(days = 365)
            user['status'] = int(self.get_arg('status', '0'))
        ps['user'] = user
        ps['roleID'] = self.get_arg('roleID', '')
        ps['userGroupID'] = self.get_arg('userGroupID', '')
        ps['userStatus'] = state.UserStatus
        ps['deps'] = department_logic.query_all_by_active()

        ps = self.format_none_to_empty(ps)
        self.render('admin/user/add_or_edit_bs.html', **ps)



    def post(self):
        ps = self.get_page_config(title = '创建用户')
        ps['ResetPasswordType'] = self.check_oper_right_custom_right(self._rightKey, self._resetPwKey)
        if ps['isedit']:
            ps['title'] = self.get_page_title('编辑用户')

        user = self.get_args(['id', 'passWord', 'name', 'realName', 'mobile', 'tel', 'email', 'remark', 'beginDate', 'endDate'], '')
        user['status'] = int(self.get_arg('status', '0'))
        user['departmentID'] = int(self.get_arg('departmentID', '0'))
        user['parentID'] = int(self.get_arg('parentID', '0'))
        ps['user'] = user
        ps['userStatus'] = state.UserStatus
        ps['roleID'] = self.get_arg('role', '')
        ps['userGroupID'] = self.get_arg('userGroup', '')
        ps['deps'] = department_logic.query_all_by_active()
        msg = self.check_str_empty_input(user, ['name', 'realName', 'email', 'mobile', 'beginDate', 'endDate'])
        if str_helper.is_null_or_empty(msg) == False:
            ps['msg'] = msg
            ps = self.format_none_to_empty(ps)
            self.render('admin/user/add_or_edit_bs.html', **ps)
            return

        user['user'] = self.get_oper_user()
        ps['user'] = copy.copy(user)
        if ps['isedit']:
            self.check_oper_right(right = state.operEdit)
            try:
                ou = user_logic.query_one_by_name(name = user['name'])
                info = user_logic.update(id = user['id'], realName = user['realName'], 
                        departmentID = user['departmentID'], parentID = user['parentID'], mobile = user['mobile'], 
                        tel = user['tel'], email = user['email'], status = user['status'], beginDate = user['beginDate'], 
                        endDate = user['endDate'], remark = user['remark'], user = user['user'])
                if info:
                    nu = user_logic.query_one_by_name(name = user['name'])
                    self.bind_role(userID = nu['id'], roleID = ps['roleID'], user = user['user'])
                    self.bind_user_group(userID = nu['id'], userGroupID = ps['userGroupID'], user = user['user'])
                    self.write_oper_log(action = 'userEdit', targetType = 1, targetID = str(nu['id']), targetName = nu['name'], startStatus = str_helper.json_encode(ou), endStatus= str_helper.json_encode(nu))
                    ps = self.get_ok_and_back_params(ps = ps, refUrl = ps['refUrl'])
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        else:
            self.check_oper_right(right = state.operEdit)            
            try:
                info = user_logic.add(name = user['name'], passWord = user['passWord'], 
                            realName = user['realName'], departmentID = user['departmentID'], mobile = user['mobile'], 
                            tel = user['tel'], email = user['email'],beginDate = user['beginDate'], 
                            endDate = user['endDate'], status = user['status'], remark = user['remark'], 
                            parentID = user['parentID'], user = user['user'])
                if info > 0:
                    nu = user_logic.query_one_by_name(name = user['name'])
                    self.bind_role(userID = nu['id'], roleID = ps['roleID'], user = user['user'])
                    self.bind_user_group(userID = nu['id'], userGroupID = ps['userGroupID'], user = user['user'])
                    self.write_oper_log(action = 'userCreate', targetType = 1, targetID = str(nu['id']), targetName = nu['name'], startStatus = '', endStatus= str_helper.json_encode(nu))
                    ps = self.get_ok_and_back_params(ps = ps, refUrl = ps['refUrl'])
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        ps = self.format_none_to_empty(ps)
        self.render('admin/user/add_or_edit_bs.html', **ps)


    def bind_role(self, userID, roleID, user):
        if None == roleID or '' == roleID:
            return
        id = user_logic.bind_user_role(userID = userID, roleID = roleID, user = self.get_oper_user())
        if None != id and id > 0:
            self.write_oper_log(action = 'userBindRole', targetType = 1, targetID = str(userID), targetName = '', startStatus = str(userID), endStatus= str(roleID))

    def bind_user_group(self, userID, userGroupID, user):
        if None == userGroupID or '' == userGroupID:
            return
        id = usergroup_logic.bind_group_user(userGroupID = userGroupID, userID = userID, user = self.get_oper_user())
        if None != id and id > 0:
            self.write_oper_log(action = 'userGroupBindUser', targetType = 6, targetID = str(userGroupID), targetName = str(userID), startStatus = str(userGroupID), endStatus= str(userID))



    



class UserDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operDel
    def post(self):
        id = int(self.get_arg('id', '0'))
        user = self.get_oper_user()
        ou = user_logic.query_one(id = id)
        type = user_logic.delete(id = id, user = user)
        if type:
            try:
                self.write_oper_log(action = 'userDelete', targetType = 1, targetID = str(id), targetName = ou['name'], startStatus = str_helper.json_encode(ou), endStatus= '')
            except e:
                print e
            self.out_ok()
        else:
            self.out_fail(code = 101)

class UserDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operView
    def get(self):
        ps = self.get_page_config(title = '用户详情')
        id = int(self.get_arg('id', '0'))
        user = user_logic.query_one(id)
        if None == user:
            ps['msg'] = state.ResultInfo.get(103002, '')
            ps['gotoUrl'] = ps['siteDomain'] + 'Admin/User/List'
            user = {'id':'','name':'', 'passWord':'', 'statusname':'','mobile':'','tel':'','email':'','status':1,'lastLoginTime':'','lastLoginApp':'','lastLoginIp':'','remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}        
        ps['user'] = user
        ps = self.format_none_to_empty(ps)
        self.render('admin/user/detail_bs.html', **ps)




class UserRoleListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager.UserBindRoleManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '用户绑定角色列表')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = state.ResultInfo.get(105003, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/User/Add'
            self.render('admin/user/role_list.html', **ps)
            return
        
        user = user_logic.query_one(id = ps['userID'])
        ps['userName'] = user['name']
        ps['userRealName'] = user['realName']
        ps = self.format_none_to_empty(ps)
        self.render('admin/user/role_list_bs.html', **ps)


class UserRoleQueryHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager.UserBindRoleManager'
    _right = state.operView

    def post(self):
        ps = self.get_page_config(title = '用户绑定角色列表')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            self.out_fail(code = 105003)
            return
        
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = user_logic.query_page_user_roles(
                userID = ps['userID'], page = ps['page'], size = ps['size'])

        if None == ps['pagedata']:
            self.out_fail(code = 101)
        else:
            self.out_ok(data = ps['pagedata'])


class UserRoleBindHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager.UserBindRoleManager'
    _right = state.operEdit

    def post(self):
        userID = int(self.get_arg('userID', '0'))
        roleID = int(self.get_arg('roleID', '0'))
        if userID <= 0 or roleID <= 0:
            self.out_fail(code = 103004)
            return
        id = user_logic.bind_user_role(userID = userID, roleID = roleID, user = self.get_oper_user())
        if None != id and id > 0:
            self.write_oper_log(action = 'userBindRole', targetType = 1, targetID = str(userID), targetName = '', startStatus = str(userID), endStatus= str(roleID))
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
        ur = user_logic.get_user_role(id = id)
        type = user_logic.del_user_role(id = id, user = self.get_oper_user())
        if type:
            self.write_oper_log(action = 'userDeleteRole', targetType = 1, targetID = str(id), targetName = '', startStatus = str(ur['userID']), endStatus= str(ur['roleID']))
            self.out_ok()
        else:
            self.out_fail(code = 103006)


class UserRightDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager.UserBindRoleManager'
    _right = state.operView
    def get(self):
        ps = self.get_page_config(title = '用户应用权限信息')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = state.ResultInfo.get(103007, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/User/List'
            self.render('admin/user/right_detail_bs.html', **ps)
            return
        
        ps['appCode'] = self.get_arg('appCode', '')
        ps['apps'] = application_logic.query_all_by_active()
        if None == ps['apps'] or len(ps['apps']) <= 0:
            ps['msg'] = state.ResultInfo.get(101004, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/Application/Add'
            self.render('admin/user/right_detail_bs.html', **ps)
            return
        else:
            if '' == ps['appCode']:
                ps['appCode'] = ps['apps'][0]['code']
        
        ps['roles'] = user_logic.query_all_user_roles(
                userID = ps['userID'])
        user = user_logic.query_one(id = ps['userID'])
        ps['userName'] = user['name']
        ps['userRealName'] = user['realName']
        ps['userGroups'] = usergroup_logic.query_all_user_groups(
                userID = ps['userID'])
        
        ps = self.format_none_to_empty(ps)
        funcs = user_logic.query_user_app_right(userID = ps['userID'], appCode = ps['appCode'])
        ps['funcs'] = funcs
        
        self.render('admin/user/right_detail_bs.html', **ps)


class UserUserGroupListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindUserManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '用户绑定用户组列表')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:
            ps['msg'] = state.ResultInfo.get(103007, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/User/List'
            self.render('admin/user/group_list_bs.html', **ps)
            return
        
        user = user_logic.query_one(id = ps['userID'])
        ps['userName'] = user['name']
        ps['userRealName'] = user['realName']

        ps['page'] = int(self.get_arg('page', '1'))        
        ps = self.format_none_to_empty(ps)        
        self.render('admin/user/group_list_bs.html', **ps)


class UserUserGroupQueryHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserGroupManager.UserGroupBindUserManager'
    _right = state.operView

    def post(self):
        ps = self.get_page_config(title = '用户绑定用户组列表')
        ps['userID'] = int(self.get_arg('userID', '0'))
        if 0 == ps['userID']:            
            self.out_fail(code = 103007)
            return
        
        user = user_logic.query_one(id = ps['userID'])
        ps['page'] = int(self.get_arg('page', '1'))

        ps['pagedata'] = usergroup_logic.query_page_user_groups(
                userID = ps['userID'], page = ps['page'], size = ps['size'])
        
        self.out_ok(data = ps['pagedata'])


class UserResetPassWordHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operView

    def post(self):
        # ps = self.get_page_config(title = '重置用户密码')
        name = self.get_arg('name', '')

        type = self.check_oper_right_custom_right(self._rightKey, self._resetPwKey)
        if type == False:
            self.out_fail(code = 1004)
            self.finish()
            return
        # userName = self.get_arg('userName', '')
        if None == name or '' == name:
            self.out_fail(code = 103007)
            return
        
        newPW = user_logic.reset_password(name)
        if None == newPW or '' == newPW:
            self.out_fail(code = 101)
            return

        ou = user_logic.query_one_by_name(name = name)
        self.write_oper_log(action = 'userResetPw', targetType = 1, targetID = str(ou['id']), targetName = name, startStatus = '', endStatus= '')
        self.out_ok(data = '{"newpw":"'+newPW+'"}')


#导出用户excel
class UserExportHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operView
    def get(self):

        type = self.check_oper_right_custom_right(self._rightKey, self._exportUserKey)
        if type == False:
            self.redirect(config.SOCRightConfig['siteDomain']+'Admin/NotRight')
            return

        import sys
        reload(sys)                        
        sys.setdefaultencoding('utf-8')    
        ps = self.get_page_config(title = '导出用户Excel')
        user = self.get_args(['id', 'realName', 'name', 'tel', 'mobile', 'email', 'createTimeBegin', 'createTimeEnd', 'lastUpdateTimeBegin', 'lastUpdateTimeEnd'], '')
        user['status'] = int(self.get_arg('status', '0'))
        user['departmentID'] = int(self.get_arg('departmentID', '0'))
        ps['deps'] = department_logic.query_all_by_active()
        ps['page'] = int(self.get_arg('page', '1'))
        ps['userStatus'] = state.UserStatus
        ps['pagedata'] = user_logic.query_page(id = user['id'],
                    name = user['name'], realName = user['realName'], departmentID = user['departmentID'],
                     tel = user['tel'], mobile = user['mobile'], email = user['email'], 
                     status = user['status'], createTimeBegin = user['createTimeBegin'], createTimeEnd = user['createTimeEnd'], lastUpdateTimeBegin = user['lastUpdateTimeBegin'], lastUpdateTimeEnd = user['lastUpdateTimeEnd'], page = ps['page'], size = 9999)

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


class UserUnLockHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operDel
    def post(self):
        type = self.check_oper_right_custom_right(self._rightKey, self._lockUserKey)
        if type == False:
            self.out_fail(code = 1004)
            return
        id = int(self.get_arg('id', '0'))
        user = self.get_oper_user()
        ou = user_logic.query_one(id = id)
        type = user_logic.update_status(id = id, status = 1, user = user)
        if type:
            try:
                self.write_oper_log(action = 'userUnLock', targetType = 1, targetID = str(id), targetName = ou['name'], startStatus = str_helper.json_encode(ou), endStatus= '')
            except e:
                print e
            self.out_ok()
        else:
            self.out_fail(code = 101)


class UserLockHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.UserManager'
    _right = state.operDel
    def post(self):
        type = self.check_oper_right_custom_right(self._rightKey, self._lockUserKey)
        if type == False:
            self.out_fail(code = 1004)
            return
        id = int(self.get_arg('id', '0'))
        user = self.get_oper_user()
        ou = user_logic.query_one(id = id)
        type = user_logic.update_status(id = id, status = 3, user = user)
        if type:
            try:
                self.write_oper_log(action = 'userLock', targetType = 1, targetID = str(id), targetName = ou['name'], startStatus = str_helper.json_encode(ou), endStatus= '')
            except e:
                print e
            self.out_ok()
        else:
            self.out_fail(code = 101)

        

