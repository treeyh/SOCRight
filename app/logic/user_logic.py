#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, ssostatus, redis_cache, ssoerror

import config

from logic import usergroup_logic, role_logic, func_logic, application_logic

class UserLogic():

    def __init__(self):   
        return

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def _format_user_password_md5(password):
        str = '#!@81%sjl=)k' % password
        return str_helper.str_md5(str)


    _login_sql = '''  select id, realName, email, mobile, tel , name from sso_user where name = %s and passWord = %s and status != %s and isDelete = %s   '''
    _login_col = str_helper.format_str_to_list_filter_empty('id, realName, email, mobile, tel , name', ',')
    def login(self, name, password):
        password = UserLogic._format_user_password_md5(password)        
        user = mysql.find_one(self._login_sql, (name, password, ssostatus.User['leave'], ssostatus.Boole['false']), self._login_col)
        return user


    def get_goto_user_url(self, userID, appCode, ip, backUrl = ''):
        '''   
            保存为这样的格式：
            {"id": 1, "tel": "123", "email": "treeyh@126.com", "name": "\u4f59\u6d77", "rights": 
                [{"id":12, "path":"xx.aa", "realName":"abc","right":1, "customRight": [1,2,3]}, {"id":13, "path":"xx.aa.bb","right":1, "customRight": []}]}

    {"code":0,"msg":"OK","data":{"tel": "123", "name": "yuhai", "rights": [{"path": "SOCRight.Login", "right": 15, "id": 18, "customRight": []}, 
{"path": "SOCRight.AppManager", "right": 15, "id": 9, "customRight": []}, {"path": "SOCRight.FuncManager", "right": 15, "id": 10, "customRight": [1, 2]},
{"path": "SOCRight.UserManager", "right": 15, "id": 11, "customRight": []}, {"path": "SOCRight.UserManager.UserBindRoleManager", "right": 15, "id": 14, "customRight": []},
 {"path": "SOCRight.UserGroupManager", "right": 15, "id": 12, "customRight": []}, 
{"path": "SOCRight.UserGroupManager.UserGroupBindRoleManager", "right": 15, "id": 15, "customRight": []}, 
{"path": "SOCRight.UserGroupManager.UserGroupBindUserManager", "right": 15, "id": 16, "customRight": []}, {"path": "SOCRight.RoleManager", "right": 15, "id": 13, "customRight": []}, 
{"path": "SOCRight.RoleManager.RoleBindRightManager", "right": 15, "id": 17, "customRight": []}], "mobile": "123", "id": 1, "email": "treeyh@126.com", "realName": "\u4f59\u6d77"}}
        '''
        u = self.query_one(userID)
        if None == u:
            return None
        user = {}
        user['id'] = u['id']
        user['realName'] = u['realName']
        user['email'] = u['email']
        user['mobile'] = u['mobile']
        user['tel'] = u['tel']
        user['name'] = u['name']

        funcs = self.query_user_app_right(userID = userID, appCode = appCode)
        rights = []
        rightType = False
        if None != funcs and len(funcs) > 0:
            for func in funcs:
                right = {}
                right['id'] = func['id']
                right['path'] = func['path']
                right['right'] = func.get('right', 0)
                if right['right'] > 0 and not rightType:
                    rightType = True
                cr = []
                if func['customJson'] != None:
                    for j in func['customJson']:
                        if j['right']:
                            cr.append(j['id'])
                right['customRight'] = cr
                rights.append(right)
        
        user['rights'] = rights 
        uuid = str_helper.get_uuid()            
        redis_cache.setObj(uuid, user, config.cache['userRightTimeOut'])
        params = {'token':uuid}
        if backUrl != '':
            gotoUrl = str_helper.format_url(url = backUrl, params = params)
        else:
            app = application_logic.ApplicationLogic.instance().query_one(code = appCode)
            gotoUrl = str_helper.format_url(url = app['url'], params = params)
        self.update_goto_app(name = user['name'], appCode = appCode, ip = ip)
        return gotoUrl


    _query_sql = '''  select id , name, realName, parentID, mobile, tel, email, status, lastLoginTime, 
                            lastLoginApp, lastLoginIp, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime 
                    from sso_user where isDelete = %s  '''
    _query_col = str_helper.format_str_to_list_filter_empty('id , name, realName, parentID, mobile, tel, email, status, lastLoginTime, lastLoginApp, lastLoginIp, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime', ',')
    def query_page(self, id = '', name = '', realName = '', tel = '', mobile = '', email = '', status = 0, page = 1, size = 12):
        sql = self._query_sql
        isdelete = ssostatus.Boole['false']
        ps = [isdelete]
        if '' != id:
            sql = sql + ' and id = %s '
            ps.append(id)
        if 0 != status:
            sql = sql + ' and status = %s '
            ps.append(status)
        if '' != name:
            sql = sql + ' and name like %s '
            ps.append('%'+name+'%')
        if '' != realName:
            sql = sql + ' and realName like %s '
            ps.append('%'+realName+'%')
        if '' != tel:
            sql = sql + ' and tel like %s '
            ps.append('%'+tel+'%')
        if '' != email:
            sql = sql + ' and email like %s '
            ps.append('%'+email+'%')
        if '' != mobile:
            sql = sql + ' and mobile like %s '
            ps.append('%'+mobile+'%')
        yz = tuple(ps)
        sql = sql + ' order by id desc '
        users = mysql.find_page(sql, yz, self._query_col, page, size)
        if None != users['data']:
            for r in users['data']:
                r['statusname'] = ssostatus.UserStatus.get(r['status'])
        return users


    def query_one(self, id = 0):
        sql = self._query_sql
        isdelete = ssostatus.Boole['false']
        ps = [isdelete]        
        if 0 != id:
            sql = sql + ' and id = %s '
            ps.append(id)
        else:
            return None
        yz = tuple(ps)
        user = mysql.find_one(sql, yz, self._query_col)
        if None != user:
            user['statusname'] = ssostatus.UserStatus.get(user['status'])
        return user


    def query_one_by_email(self, email = ''):
        sql = self._query_sql
        isdelete = ssostatus.Boole['false']
        sql = sql + ' and email = %s '        
        yz = (isdelete, email)

        user = mysql.find_one(sql, yz, self._query_col)
        if None != user:
            user['statusname'] = ssostatus.UserStatus.get(user['status'])
        return user


    def query_one_by_name(self, name = ''):
        sql = self._query_sql
        isdelete = ssostatus.Boole['false']
        sql = sql + ' and name = %s '        
        yz = (isdelete, name)

        user = mysql.find_one(sql, yz, self._query_col)
        if None != user:
            user['statusname'] = ssostatus.UserStatus.get(user['status'])
        return user

    _add_sql = '''  INSERT INTO sso_user(name, passWord, realName, parentID, mobile, tel, email, status, lastLoginTime, 
                    lastLoginApp, lastLoginIp, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime)
                     VALUES(%s, %s, %s, %s, %s, %s, %s ,%s, null, null, null, %s, %s, %s, now(), %s, now() )  '''
    def add(self, name, passWord, realName, mobile, tel, email, status, remark, parentID, user):
        u = self.query_one_by_email(email)               #判断用户邮箱是否已存在        
        if None != u:
            raise ssoerror.SsoError(code = 103001)
        u = self.query_one_by_name(name)               #判断用户名是否已存在
        if None != u:
            raise ssoerror.SsoError(code = 103008)

        isdelete = ssostatus.Boole['false']
        passWord = self._format_user_password_md5(passWord)
        yz = (name, passWord, realName, parentID, mobile, tel, email, status, remark, isdelete, user, user)
        uid = mysql.insert_or_update_or_delete(self._add_sql, yz, True)
        return uid


    _update_sql = '''   update sso_user set  `realName` = %s, `parentID` = %s, `mobile` = %s, `tel` = %s, `email` = %s,
                            `status` = %s, `remark` = %s, `lastUpdater` = %s, 
                            `lastUpdateTime` = now() where `id` = %s  '''
    def update(self, id, realName, parentID, mobile, tel, email, status, remark, user):
        u = self.query_one_by_email(email)               #判断用户邮箱是否已存在     
        if None != u and str(u['id']) != str(id):
            raise ssoerror.SsoError(code = 103001)

        isdelete = ssostatus.Boole['false']
        yz = (realName, parentID, mobile, tel, email, status, remark, user, id)
        result = mysql.insert_or_update_or_delete(self._update_sql, yz)
        return 0 == result

    
    _delete_sql = '''   update sso_user set isDelete = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where id = %s  '''
    def delete(self, id, user):
        isdelete = ssostatus.Boole['true']
        yz = (isdelete, user, id)
        result = mysql.insert_or_update_or_delete(self._delete_sql, yz)
        return 0 == result


    

    _update_password_sql = '''   update sso_user set  `passWord` = %s where  `name` = %s and isDelete = %s '''
    def update_password(self, name , oldPassWord, newPassWord1, newPassWord2):
        if newPassWord1 != newPassWord2:
            raise ssoerror.SsoError(code = 103010)
        u = self.login(name, oldPassWord)               #旧密码是否正确     
        if None == u:
            raise ssoerror.SsoError(code = 103009)

        isdelete = ssostatus.Boole['false']
        pw = self._format_user_password_md5(newPassWord1)
        yz = (pw, name, isdelete)
        result = mysql.insert_or_update_or_delete(self._update_password_sql, yz)
        return 0 == result



    _update_goto_app_sql = '''   update sso_user set  `lastLoginTime` = now(), `lastLoginApp` = %s, `lastLoginIp` = %s where  `name` = %s and isDelete = %s '''
    def update_goto_app(self, name , appCode, ip):
        
        isdelete = ssostatus.Boole['false']
        yz = (appCode, ip, name, isdelete)
        result = mysql.insert_or_update_or_delete(self._update_goto_app_sql, yz)
        return 0 == result

    
    _query_user_roles_sql = '''  select ugu.id, ugu.userID, ugu.roleID, ugu.remark, ugu.isDelete, ugu.creater, 
                            ugu.createTime, ugu.lastUpdater, ugu.lastUpdateTime, u.`name` as roleName from sso_user_role as ugu 
                            LEFT JOIN sso_role u on u.id = ugu.roleID 
                            where ugu.userID = %s and  ugu.isDelete = %s and u.status = %s order by ugu.id desc '''
    _query_user_roles_col = str_helper.format_str_to_list_filter_empty(
            'id, userID, roleID, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime, roleName', ',')
    def query_page_user_roles(self, userID, page = 1, size = 12):
        isdelete = ssostatus.Boole['false']
        yz = (userID, isdelete, ssostatus.statusActive)
        roles = mysql.find_page(self._query_user_roles_sql, yz, self._query_user_roles_col, page, size)
        return roles

    def query_all_user_roles(self, userID):
        isdelete = ssostatus.Boole['false']
        yz = (userID, isdelete, ssostatus.statusActive)
        roles = mysql.find_all(self._query_user_roles_sql, yz, self._query_user_roles_col)
        return roles


    _bind_group_role_sql = '''  INSERT INTO sso_user_role(userID, roleID, remark, isDelete, creater, 
            createTime, lastUpdater, lastUpdateTime) VALUES(%s, %s, %s, %s, %s, NOW(), %s, NOW()) '''
    def bind_user_role(self, userID, roleID, user):
        roles = self.query_all_user_roles(userID)
        if roles != None:
            for role in roles:
                if role['roleID'] == roleID:
                    return True
        isdelete = ssostatus.Boole['false']
        yz = (userID, roleID, '', isdelete, user, user)
        result = mysql.insert_or_update_or_delete(self._bind_group_role_sql, yz)
        return 0 == result


    _del_user_role_sql = '''  update sso_user_role set isDelete = %s , lastUpdater = %s , lastUpdateTime = now() WHERE id = %s '''
    def del_user_role(self, id, user):
        isdelete = ssostatus.Boole['true']
        yz = (isdelete, user, id)
        result = mysql.insert_or_update_or_delete(self._del_user_role_sql, yz)
        return 0 == result



    def query_user_app_right(self, userID, appCode):
        user = self.query_one(userID)
        if user == None:
            return None
        funcs = func_logic.FuncLogic.instance().query_all_by_app(appCode)
        if None == funcs or len(funcs) <= 0:
            return None

        '''  初始化权限  '''
        funcs = role_logic.RoleLogic.instance().init_func_right(funcs)
        
        '''  统计绑定的用户组权限  '''
        userGroups = usergroup_logic.UserGroupLogic.instance().query_all_user_groups(userID)        
        if userGroups != None and len(userGroups) > 0:
            for userGroup in userGroups:
                funcs = usergroup_logic.UserGroupLogic.instance().query_user_group_app_right(userGroupID = userGroup['userGroupID'], appCode = appCode, funcs = funcs)
        
        '''  统计绑定的角色权限  '''
        roles = self.query_all_user_roles(userID)
        print roles
        if None != roles and len(roles) > 0:
            for role in roles:
                funcs = role_logic.RoleLogic.instance().format_role_func_right(appCode = appCode, roleID = role['roleID'], funcs = funcs)
        return funcs