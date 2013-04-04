#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error

from logic import func_logic, role_logic

class UserGroupLogic():

    def __init__(self):   
        return

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance



    _query_sql = '''  select id, name, status, remark, isDelete, creater, createTime, 
                        lastUpdater, lastUpdateTime from sso_user_group where isDelete = %s  '''
    _query_col = str_helper.format_str_to_list_filter_empty('id, name, status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime', ',')
    def query_page(self, id = '', name = '', status = 0, page = 1, size = 12):
        sql = self._query_sql
        isdelete = state.Boole['false']
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
        yz = tuple(ps)
        sql = sql + ' order by id desc '
        usergroups = mysql.find_page(sql, yz, self._query_col, page, size)
        if None != usergroups['data']:
            for r in usergroups['data']:
                r['statusname'] = state.Status.get(r['status'])
        return usergroups

    def query_all_by_active(self):
        isdelete = state.Boole['false']
        sql = self._query_sql + ' and status = %s order by id desc '
        yz = (isdelete, state.statusActive)
        usergroups = mysql.find_all(sql, yz, self._query_col)
        if None != usergroups:
            for r in usergroups:
                r['statusname'] = state.Status.get(r['status'])
        return usergroups

    def query_one(self, id = 0):
        sql = self._query_sql
        isdelete = state.Boole['false']
        ps = [isdelete]        
        if 0 != id:
            sql = sql + ' and id = %s '
            ps.append(id)
        else:
            return None
        yz = tuple(ps)
        usergroup = mysql.find_one(sql, yz, self._query_col)
        if None != usergroup:
            usergroup['statusname'] = state.Status.get(usergroup['status'])
        return usergroup


    def query_one_by_name(self, name = ''):
        sql = self._query_sql
        isdelete = state.Boole['false']
        sql = sql + ' and name = %s '
        yz = (isdelete, name)
        usergroup = mysql.find_one(sql, yz, self._query_col)
        if None != usergroup:
            usergroup['statusname'] = state.Status.get(usergroup['status'])
        return usergroup



    _add_sql = '''  INSERT INTO sso_user_group(name, status, remark, isDelete, 
                        creater, createTime, lastUpdater, lastUpdateTime)
                     VALUES(%s, %s, %s, %s, %s, now(), %s, now() )  '''
    def add(self, name, status, remark, user):
        obj = self.query_one_by_name(name = name)
        if None != obj:
            raise  error.RightError(code = 105001)

        isdelete = state.Boole['false']
        yz = (name, status, remark, isdelete, user, user)
        ugid = mysql.insert_or_update_or_delete(self._add_sql, yz, True)
        return ugid


    _update_sql = '''   update sso_user_group set name = %s, status = %s, remark = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where id = %s  '''
    def update(self, id, name, status, remark, user):
        obj = self.query_one_by_name(name = name)
        if None != obj and str(obj['id']) == str(id):
            raise  error.RightError(code = 105001)

        isdelete = state.Boole['false']
        yz = (name, status, remark, user, id)
        result = mysql.insert_or_update_or_delete(self._update_sql, yz)
        return 0 == result

    
    _delete_sql = '''   update sso_user_group set isDelete = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where id = %s  '''
    def delete(self, id, user):
        isdelete = state.Boole['true']
        yz = (isdelete, user, id)
        result = mysql.insert_or_update_or_delete(self._delete_sql, yz)
        return 0 == result


    
    _query_group_users_sql = '''  select ugu.id, ugu.userGroupID, ugu.userID, ugu.remark, ugu.isDelete, ugu.creater, 
                            ugu.createTime, ugu.lastUpdater, ugu.lastUpdateTime, u.`name` as userName, u.`email` as userEmail, u.`realName` as userRealName from sso_user_group_user as ugu 
                            LEFT JOIN sso_user u on u.id = ugu.userID 
                            where  ugu.userGroupID = %s and  ugu.isDelete = %s and u.status = %s  order by ugu.id desc '''
    _query_group_users_col = str_helper.format_str_to_list_filter_empty(
            'id, userGroupID, userID, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime, userName, userEmail, userRealName', ',')
    def query_page_group_users(self, userGroupID, page = 1, size = 12):
        isdelete = state.Boole['false']
        yz = (userGroupID, isdelete, state.statusActive)
        users = mysql.find_page(self._query_group_users_sql, yz, self._query_group_users_col, page, size)
        return users

    def query_all_group_users(self, userGroupID):
        isdelete = state.Boole['false']
        yz = (userGroupID, isdelete, state.statusActive)
        users = mysql.find_all(self._query_group_users_sql, yz, self._query_group_users_col)
        return users
    


    _query_user_groups_sql = '''  select ugu.id, ugu.userGroupID, ugu.userID, ugu.remark, ugu.isDelete, ugu.creater, 
                            ugu.createTime, ugu.lastUpdater, ugu.lastUpdateTime, u.`name` as userGroupName from sso_user_group_user as ugu 
                            LEFT JOIN sso_user_group u on u.id = ugu.userGroupID 
                            where  ugu.userID = %s and  ugu.isDelete = %s and u.status = %s order by ugu.id desc '''
    _query_user_groups_col = str_helper.format_str_to_list_filter_empty(
            'id, userGroupID, userID, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime, userGroupName', ',')
    def query_all_user_groups(self, userID):
        isdelete = state.Boole['false']
        yz = (userID, isdelete, state.statusActive)
        users = mysql.find_all(self._query_user_groups_sql, yz, self._query_user_groups_col)
        return users

    def query_page_user_groups(self, userID, page = 1, size = 12):
        isdelete = state.Boole['false']
        yz = (userID, isdelete, state.statusActive)
        users = mysql.find_page(self._query_user_groups_sql, yz, self._query_user_groups_col, page, size)
        return users



    _bind_group_user_sql = '''  INSERT INTO sso_user_group_user(userGroupID, userID, remark, isDelete, creater, 
            createTime, lastUpdater, lastUpdateTime) VALUES(%s, %s, %s, %s, %s, NOW(), %s, NOW()) '''
    def bind_group_user(self, userGroupID, userID, user):
        users = self.query_all_group_users(userGroupID)
        if users != None:
            for u in users:
                if u['userID'] == userID:
                    return True
        isdelete = state.Boole['false']
        yz = (userGroupID, userID, '', isdelete, user, user)
        result = mysql.insert_or_update_or_delete(self._bind_group_user_sql, yz, True)
        return result > 0


    _del_group_user_sql = '''  update sso_user_group_user set isDelete = %s , lastUpdater = %s , lastUpdateTime = now() WHERE id = %s '''
    def del_group_user(self, id, user):
        isdelete = state.Boole['true']
        yz = (isdelete, user, id)
        result = mysql.insert_or_update_or_delete(self._del_group_user_sql, yz)
        return result == 0



    
    _query_group_roles_sql = '''  select ugu.id, ugu.userGroupID, ugu.roleID, ugu.remark, ugu.isDelete, ugu.creater, 
                            ugu.createTime, ugu.lastUpdater, ugu.lastUpdateTime, u.`name` as roleName from sso_user_group_role as ugu 
                            LEFT JOIN sso_role u on u.id = ugu.roleID 
                            where ugu.userGroupID = %s and  ugu.isDelete = %s and u.status = %s  order by ugu.id desc '''
    _query_group_roles_col = str_helper.format_str_to_list_filter_empty(
            'id, userGroupID, roleID, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime, roleName', ',')
    def query_page_group_roles(self, userGroupID, page = 1, size = 12):
        isdelete = state.Boole['false']
        yz = (userGroupID, isdelete, state.statusActive)
        roles = mysql.find_page(self._query_group_roles_sql, yz, self._query_group_roles_col, page, size)
        return roles

    def query_all_group_roles(self, userGroupID):
        isdelete = state.Boole['false']
        yz = (userGroupID, isdelete, state.statusActive)
        roles = mysql.find_all(self._query_group_roles_sql, yz, self._query_group_roles_col)
        return roles


    _bind_group_role_sql = '''  INSERT INTO sso_user_group_role(userGroupID, roleID, remark, isDelete, creater, 
            createTime, lastUpdater, lastUpdateTime) VALUES(%s, %s, %s, %s, %s, NOW(), %s, NOW()) '''
    def bind_group_role(self, userGroupID, roleID, user):
        roles = self.query_all_group_roles(userGroupID)
        if roles != None:
            for r in roles:
                if r['roleID'] == roleID:
                    return True
        isdelete = state.Boole['false']
        yz = (userGroupID, roleID, '', isdelete, user, user)
        result = mysql.insert_or_update_or_delete(self._bind_group_role_sql, yz)
        return 0 == result


    _del_group_role_sql = '''  update sso_user_group_role set isDelete = %s , lastUpdater = %s , lastUpdateTime = now() WHERE id = %s '''
    def del_group_role(self, id, user):
        isdelete = state.Boole['true']
        yz = (isdelete, user, id)
        result = mysql.insert_or_update_or_delete(self._del_group_role_sql, yz)
        return 0 == result


    
    
    def query_user_group_app_right(self, userGroupID, appCode, funcs = None):
        '''查询用户组对应应用的权限信息'''
        if None == funcs:
            funcs = func_logic.FuncLogic.instance().query_all_by_app(appCode)
            funcs = role_logic.RoleLogic.instance().init_func_right(funcs)
        if funcs == None or len(funcs) <= 0:
            return funcs

        roles = self.query_all_group_roles(userGroupID)
        if None == roles or len(roles) <= 0:
            return funcs
        for role in roles:
            funcs = role_logic.RoleLogic.instance().format_role_func_right(appCode=appCode, roleID = role['roleID'], funcs = funcs)

        return funcs