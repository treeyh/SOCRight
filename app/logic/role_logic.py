#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error


_query_sql = '''  select id, name, status, remark, isDelete, creater, createTime, 
                    lastUpdater, lastUpdateTime from sso_role where isDelete = %s  '''
_query_col = str_helper.format_str_to_list_filter_empty('id, name, status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime', ',')
''' 分页查询角色信息 '''
def query_page( id = '', name = '', status = 0, page = 1, size = 12):
    sql = _query_sql
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
    roles = mysql.find_page(sql, yz, _query_col, page, size)
    if None != roles['data']:
        for r in roles['data']:
            r['statusname'] = state.Status.get(r['status'])
    return roles

''' 根据id查询角色 '''
def query_one( id = 0):
    sql = _query_sql
    isdelete = state.Boole['false']
    ps = [isdelete]        
    if 0 != id:
        sql = sql + ' and id = %s '
        ps.append(id)
    else:
        return None
    yz = tuple(ps)
    role = mysql.find_one(sql, yz, _query_col)
    if None != role:
        role['statusname'] = state.Status.get(role['status'])
    return role

''' 根据名称查询角色 '''
def query_one_by_name( name = ''):
    sql = _query_sql
    isdelete = state.Boole['false']
    sql = sql + ' and name = %s '
    yz = (isdelete, name)
    role = mysql.find_one(sql, yz, _query_col)
    if None != role:
        role['statusname'] = state.Status.get(role['status'])
    return role


_query_all_by_active_sql = '''  select id, name from sso_role where isDelete = %s and status = %s  '''
_query_all_by_active_col = str_helper.format_str_to_list_filter_empty('id, name', ',')
''' 获取所有可用的角色 '''
def query_all_by_active():
    sql = _query_all_by_active_sql
    isdelete = state.Boole['false']
    yz = (isdelete, state.statusActive)
    roles = mysql.find_all(sql, yz, _query_all_by_active_col)
    return roles



_add_sql = '''  INSERT INTO sso_role(name, status, remark, isDelete, 
                    creater, createTime, lastUpdater, lastUpdateTime)
                 VALUES(%s, %s, %s, %s, %s, now(), %s, now() )  '''
''' 创建角色 '''
def add( name, status, remark, user):
    obj = query_one_by_name(name = name)
    if None != obj:
        raise error.RightError(code = 104001)

    isdelete = state.Boole['false']
    yz = (name, status, remark, isdelete, user, user)
    uid = mysql.insert_or_update_or_delete(_add_sql, yz, True)
    return uid


_update_sql = '''   update sso_role set name = %s, status = %s, remark = %s, lastUpdater = %s, 
                        lastUpdateTime = now() where id = %s  '''
''' 更新角色 '''
def update( id, name, status, remark, user):
    obj = query_one_by_name(name = name)
    if None != obj and str(obj['id']) != str(id):
        raise error.RightError(code = 104001)
        
    isdelete = state.Boole['false']
    yz = (name, status, remark, user, id)
    result = mysql.insert_or_update_or_delete(_update_sql, yz)
    return 0 == result


_delete_sql = '''   update sso_role set isDelete = %s, lastUpdater = %s, 
                        lastUpdateTime = now() where id = %s  '''
''' 删除角色 '''
def delete( id, user):
    isdelete = state.Boole['true']
    yz = (isdelete, user, id)
    result = mysql.insert_or_update_or_delete(_delete_sql, yz)
    return 0 == result




_delete_user_bind_role_sql = ''' update sso_user_role set isDelete = %s, lastUpdater = %s, 
                        lastUpdateTime = now()  where roleID = %s and userID = %s and isDelete = %s '''
_delete_user_bind_user_group_sql = ''' update  sso_user_group_user set isDelete = %s, lastUpdater = %s, 
                        lastUpdateTime = now()  where userID = %s and isDelete = %s and userGroupID in 
                        (select userGroupID from sso_user_group_role where roleID = %s)  '''
''' 删除用户与角色的关联，通过用户组的间接关联也删除 '''
def delete_user_bind(userID , roleID , user):
    istruedelete = state.Boole['true']
    isfalsedelete = state.Boole['false']
    yz = (istruedelete, user, roleID, userID, isfalsedelete)
    result = mysql.insert_or_update_or_delete(_delete_user_bind_role_sql, yz)

    yz2 = (istruedelete, user, userID, isfalsedelete, roleID)
    result2 = mysql.insert_or_update_or_delete(_delete_user_bind_user_group_sql, yz2)
    return 0 == result and 0 == result2





_query_right_by_role_app_sql = '''  select rr.id, rr.funcID, rr.appCode, rr.roleID, rr.`right`, rr.customRight, rr.isDelete, rr.creater, 
                    rr.createTime, rr.lastUpdater, rr.lastUpdateTime, f.path from sso_role_right as rr  left  join  sso_func  as  f  on  rr.funcID = f.id 
                    where rr.isDelete = %s and rr.roleID = %s and rr.appCode = %s '''
_query_right_by_role_app_col = str_helper.format_str_to_list_filter_empty('id, funcID, appCode, roleID, right, customRight, isDelete, creater, createTime, lastUpdater, lastUpdateTime, path', ',')
''' 查询角色 '''
def query_right_by_role_app( roleID, appCode):
    sql = _query_right_by_role_app_sql
    isdelete = state.Boole['false']
    yz = (isdelete, roleID, appCode)
    roles = mysql.find_all(sql, yz, _query_right_by_role_app_col)
    return roles


_delete_right_by_role_app_sql = '''  update sso_role_right set isDelete = %s , lastUpdater = %s, lastUpdateTime = now() 
                    where isDelete = %s and roleID = %s and appCode = %s '''    
''' 删除角色的应用权限 '''
def delete_right_by_role_app( roleID, appCode, user):
    sql = _delete_right_by_role_app_sql
    isdeletetrue = state.Boole['true']
    isdeletefalse = state.Boole['false']
    yz = (isdeletetrue, user, isdeletefalse, roleID, appCode)
    result = mysql.insert_or_update_or_delete(sql, yz)
    return 0 == result


_add_right_by_role_app_sql = '''  insert into sso_role_right(funcID, appCode, roleID, `right`, customRight, isDelete, creater, 
                    createTime, lastUpdater, lastUpdateTime) values(%s, %s, %s, %s, %s, %s, %s, now(), %s, now()) '''    
''' 添加角色的应用权限 '''
def add_right_by_role_app( roleID, appCode, rights, user):
    delete_right_by_role_app(roleID, appCode, user)
    
    sql = _add_right_by_role_app_sql
    isdelete = state.Boole['false']
    params = []
    for right in rights:
        params.append( (right['funcID'], appCode, roleID, right['right'], right['customRight'], isdelete, user, user))
    result = mysql.insert_more(sql, params)
    return 0 == result


''' 格式化角色的功能权限列表 '''
def format_role_func_right( appCode, roleID, funcs):
    '''格式化角色对应该应用的权限信息'''
    if None == funcs or len(funcs) <= 0:
        return funcs

    rights = query_right_by_role_app(roleID = roleID, appCode = appCode)
    if None == rights or len(rights) <= 0 :
        return funcs
    m = {}
    if None != rights and len(rights) > 0:
        for r in rights:
            m[r['path']] = r
    for func in funcs:              #格式化权限信息
        path = func['path']
        right = m.get(path, None)
        if None != right:
            func['right'] = func['right'] | right.get('right', 0)
        if None != func['customJson']:
            for custom in func['customJson']:
                if (None != right) and ((',%s,' % custom['k']) in right.get('customRight', '')):
                    custom['right'] = True
    return funcs

''' 初始化功能权限 '''
def init_func_right( funcs):
    #初始化功能的权限信息
    if None == funcs or len(funcs) <= 0:
        return None

    for func in funcs:
        if func.get('right', None) == None:
            func['right'] = 0
        if func.get('customJson','') != '' and (isinstance(func['customJson'], str) or isinstance(func['customJson'], unicode)):
            func['customJson'] = str_helper.json_decode(func['customJson'])
            for j in func['customJson']:
                j['right'] = False
        else:
            func['customJson'] = None
    return funcs