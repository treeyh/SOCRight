#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, redis_cache, error

import config

from logic import usergroup_logic, role_logic, func_logic, application_logic


''' 获取密码md5值 '''
def _format_user_password_md5( password):
    str = '#!@81%sjl=)k' % password
    return str_helper.str_md5(str)


_pw1 = 'abcdefghijklmnopqrstuvwxyz'
_pw2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
_pw3 = '0123456789'
def _check_password_complexity( password):
    charTypeCount = 0
    if 8 > len(password):
        return 103012
    pw1 , pw2, pw3, pw4 = False , False, False, False
    for x in password:
        if x in _pw1:
            pw1 = True
        elif x in _pw2:
            pw2 = True
        elif x in _pw3:
            pw3 = True
        else:
            pw4 = True

    if (pw1 == True or pw2 == True) and pw3 == True:
        return 0
    else:
        return 103012





_login_sql = '''  select id, realName, departmentID, email, mobile, tel , name, loginCount 
                        from sso_user where name = %s and passWord = %s and status = %s and 
                        beginDate <= now() and endDate >= now() 
                        and isDelete = %s   '''
_login_col = str_helper.format_str_to_list_filter_empty('id, realName, departmentID, email, mobile, tel , name, loginCount', ',')
''' 用户登录 '''
def login( name, password):
    password = _format_user_password_md5(password)
    user = mysql.find_one(_login_sql, (name, password, state.statusActive, state.Boole['false']), _login_col)
    return user

''' 登录应用，获得登录的url '''
def get_goto_user_url( userID, appCode, ip, backUrl = ''):
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
    u = query_one(userID)
    if None == u:
        return None
    user = {}
    user['id'] = u['id']
    user['realName'] = u['realName']
    user['email'] = u['email']
    user['mobile'] = u['mobile']
    user['tel'] = u['tel']
    user['name'] = u['name']

    funcs = query_user_app_right(userID = userID, appCode = appCode)
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
                        cr.append(j['k'])
            right['customRight'] = cr
            rights.append(right)
    
    user['rights'] = rights 
    uuid = str_helper.get_uuid()            
    redis_cache.setObj(uuid, user, config.cache['userRightTimeOut'])
    params = {'token':uuid}
    if backUrl != '':
        gotoUrl = str_helper.format_url(url = backUrl, params = params)
    else:
        app = application_logic.query_one(code = appCode)
        gotoUrl = str_helper.format_url(url = app['url'], params = params)
    update_goto_app(name = user['name'], appCode = appCode, ip = ip)
    return gotoUrl


_query_sql = '''  select u.id , u.name, u.realName, u.parentID, u.departmentID, u.mobile, u.tel, u.email, u.status, u.lastLoginTime, 
                        u.lastLoginApp, u.lastLoginIp, u.loginCount, u.beginDate, u.endDate, u.remark, u.isDelete, u.creater, u.createTime, u.lastUpdater, u.lastUpdateTime, d.name as departmentName  
                from sso_user as u 
                LEFT JOIN sso_department as d ON d.id = u.departmentID 
                where u.isDelete = %s  '''
_query_col = str_helper.format_str_to_list_filter_empty('id , name, realName, parentID, departmentID, mobile, tel, email, status, lastLoginTime, lastLoginApp, lastLoginIp, loginCount, beginDate, endDate, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime, departmentName', ',')
''' 分页查询用户信息 '''
def query_page( id = '', name = '', realName = '', departmentID = 0, 
                    tel = '', mobile = '', email = '', status = 0, createTimeBegin = 0, createTimeEnd = 0, lastUpdateTimeBegin = 0, lastUpdateTimeEnd = 0, page = 1, size = 12):
    sql = _query_sql
    isdelete = state.Boole['false']
    ps = [isdelete]
    if '' != id:
        sql = sql + ' and u.id = %s '
        ps.append(id)
    if 0 != status:
        sql = sql + ' and u.status = %s '
        ps.append(status)
    if 0 != departmentID:
        sql = sql + ' and u.departmentID = %s '
        ps.append(departmentID)
    if '' != name:
        sql = sql + ' and u.name like %s '
        ps.append('%'+name+'%')
    if '' != realName:
        sql = sql + ' and u.realName like %s '
        ps.append('%'+realName+'%')
    if '' != tel:
        sql = sql + ' and u.tel like %s '
        ps.append('%'+tel+'%')
    if '' != email:
        sql = sql + ' and u.email like %s '
        ps.append('%'+email+'%')
    if '' != mobile:
        sql = sql + ' and u.mobile like %s '
        ps.append('%'+mobile+'%')
    if None != createTimeBegin and '' != createTimeBegin:
        sql = sql + ' and u.createTime >= %s '
        ps.append(createTimeBegin)
    if None != createTimeEnd and '' != createTimeEnd:
        sql = sql + ' and u.createTime <= %s '
        ps.append(createTimeEnd)
    if None != lastUpdateTimeBegin and '' != lastUpdateTimeBegin:
        sql = sql + ' and u.lastUpdateTime >= %s '
        ps.append(lastUpdateTimeBegin)
    if None != lastUpdateTimeEnd and '' != lastUpdateTimeEnd:
        sql = sql + ' and u.lastUpdateTime <= %s '
        ps.append(lastUpdateTimeEnd)
    yz = tuple(ps)
    sql = sql + ' order by u.id desc '
    users = mysql.find_page(sql, yz, _query_col, page, size)
    if None != users['data']:
        for r in users['data']:
            r['beginDate'] = str(r['beginDate'])[0:10]
            r['endDate'] = str(r['endDate'])[0:10]
            r['statusname'] = state.UserStatus.get(r['status'])
    return users


_query_role_all_user_sql = ''' select u.id , u.name, u.realName, u.parentID, u.departmentID, u.mobile, u.tel, u.email, u.status, u.lastLoginTime, 
u.lastLoginApp, u.lastLoginIp, u.loginCount, u.beginDate, u.endDate, u.remark, u.isDelete, u.creater, u.createTime, u.lastUpdater, u.lastUpdateTime , d.name as departmentName from sso_user as u 
left JOIN sso_department as d on d.id = u.departmentID 
left JOIN sso_user_role as ur on ur.userID = u.id 
where ((ur.roleID = %s and ur.isDelete = %s) or ( exists  
(select ugu.userID from sso_user_group_user ugu where ugu.userID = u.id and exists  
(select ugr.id from sso_user_group_role ugr where ugr.id = ugu.userGroupID and ugr.roleID = %s and ugr.isDelete = %s)))) 
and u.isDelete = %s  '''
''' 分页查询角色下所有用户信息 '''
def query_page_by_roleid( roleID = '', userName = '', page = 1, size = 12):
    sql = _query_role_all_user_sql
    isdelete = state.Boole['false']
    ps = [ roleID, isdelete, roleID, isdelete, isdelete ]
    if not str_helper.is_null_or_empty(userName):
        sql = sql + ' and  u.name = %s  '
        ps.append(userName)
    yz = tuple(ps)
    sql = sql + '  order by u.departmentID asc , u.id desc '
    users = mysql.find_page(sql, yz, _query_col, page, size)
    if None != users['data']:
        for r in users['data']:
            r['beginDate'] = str(r['beginDate'])[0:10]
            r['endDate'] = str(r['endDate'])[0:10]
            r['statusname'] = state.UserStatus.get(r['status'])
    return users



''' 根据userID查询用户 '''
def query_one( id = 0):
    sql = _query_sql
    isdelete = state.Boole['false']
    ps = [isdelete]        
    if 0 != id:
        sql = sql + ' and u.id = %s '
        ps.append(id)
    else:
        return None
    yz = tuple(ps)
    user = mysql.find_one(sql, yz, _query_col)
    if None != user:
        user['beginDate'] = str(user['beginDate'])[0:10]
        user['endDate'] = str(user['endDate'])[0:10]
        user['statusname'] = state.UserStatus.get(user['status'])
    return user

''' 根据email查询用户 '''
def query_one_by_email( email = ''):
    sql = _query_sql
    isdelete = state.Boole['false']
    sql = sql + ' and u.email = %s '        
    yz = (isdelete, email)

    user = mysql.find_one(sql, yz, _query_col)
    if None != user:
        user['beginDate'] = str(user['beginDate'])[0:10]
        user['endDate'] = str(user['endDate'])[0:10]
        user['statusname'] = state.UserStatus.get(user['status'])
    return user

''' 根据userName查询用户 '''
def query_one_by_name( name = ''):
    sql = _query_sql
    isdelete = state.Boole['false']
    sql = sql + ' and u.name = %s '        
    yz = (isdelete, name)

    user = mysql.find_one(sql, yz, _query_col)
    if None != user:
        user['beginDate'] = str(user['beginDate'])[0:10]
        user['endDate'] = str(user['endDate'])[0:10]
        user['statusname'] = state.UserStatus.get(user['status'])
    return user

_add_sql = '''  INSERT INTO sso_user(name, passWord, realName, departmentID, parentID, mobile, tel, email, status, lastLoginTime, 
                lastLoginApp, lastLoginIp, loginCount, beginDate, endDate, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s ,%s, null, null, null, 0, %s, %s, %s, %s, %s, now(), %s, now() )  '''
''' 创建用户 '''
def add( name, passWord, realName, departmentID, mobile, 
    tel, email, status, beginDate, endDate, remark, parentID, user):
    u = query_one_by_email(email)               #判断用户邮箱是否已存在        
    if None != u:
        raise error.RightError(code = 103001)
    u = query_one_by_name(name)               #判断用户名是否已存在
    if None != u:
        raise error.RightError(code = 103008)
    pwComp = _check_password_complexity(password = passWord)
    if pwComp != 0:
        raise error.RightError(code = pwComp)

    isdelete = state.Boole['false']
    passWord = _format_user_password_md5(passWord)
    yz = (name, passWord, realName, departmentID, parentID, mobile, tel, email, status, 
        beginDate, endDate + ' 23:59:59', remark, isdelete, user, user)
    uid = mysql.insert_or_update_or_delete(_add_sql, yz, True)
    return uid


_update_sql = '''   update sso_user set  `realName` = %s, `departmentID` = %s, `parentID` = %s, `mobile` = %s, `tel` = %s, `email` = %s,
                        `status` = %s, beginDate = %s, endDate = %s, `remark` = %s, `lastUpdater` = %s, 
                        `lastUpdateTime` = now() where `id` = %s  '''
''' 更新用户 '''
def update( id, realName, departmentID, parentID, mobile, tel, email, status,
             beginDate, endDate, remark, user):
    u = query_one_by_email(email)               #判断用户邮箱是否已存在     
    if None != u and str(u['id']) != str(id):
        raise error.RightError(code = 103001)

    isdelete = state.Boole['false']
    yz = (realName, departmentID, parentID, mobile, tel, email, 
        status, beginDate, endDate + ' 23:59:59', remark, user, id)
    result = mysql.insert_or_update_or_delete(_update_sql, yz)
    return 0 == result


_delete_sql = '''   update sso_user set isDelete = %s, lastUpdater = %s, 
                        lastUpdateTime = now() where id = %s  '''
''' 删除用户，逻辑删除 '''
def delete( id, user):
    isdelete = state.Boole['true']
    yz = (isdelete, user, id)
    result = mysql.insert_or_update_or_delete(_delete_sql, yz)
    return 0 == result




_update_password_sql = '''   update sso_user set  `passWord` = %s where  `name` = %s and isDelete = %s '''
''' 修改用户密码 '''
def update_password( name , oldPassWord, newPassWord1, newPassWord2):
    if newPassWord1 != newPassWord2:
        raise error.RightError(code = 103010)
    if oldPassWord == newPassWord1:
        raise error.RightError(code = 103011)
    pwComp = _check_password_complexity(password = newPassWord1)
    if pwComp != 0:
        raise error.RightError(code = pwComp)
    u = login(name, oldPassWord)               #旧密码是否正确     
    if None == u:
        raise error.RightError(code = 103009)

    isdelete = state.Boole['false']
    pw = _format_user_password_md5(newPassWord1)
    yz = (pw, name, isdelete)
    result = mysql.insert_or_update_or_delete(_update_password_sql, yz)
    return 0 == result


''' 重置用户密码 '''
def reset_password( name):
    passWord = str_helper.get_uuid()
    isdelete = state.Boole['false']
    pw = _format_user_password_md5(passWord)        
    yz = (pw, name, isdelete)

    result = mysql.insert_or_update_or_delete(_update_password_sql, yz)
    
    if 0 == result:
        return passWord
    return None


_update_status_sql = '''   update sso_user set  `status` = %s, `lastUpdater` = %s, 
                        `lastUpdateTime` = now() where `id` = %s  '''
''' 更新用户 '''
def update_status( id, status, user):
    yz = (status, user, id)
    result = mysql.insert_or_update_or_delete(_update_status_sql, yz)
    return 0 == result


_update_goto_app_sql = '''   update sso_user set  `lastLoginTime` = now(), `lastLoginApp` = %s, `lastLoginIp` = %s, 
                                `loginCount` = `loginCount` + 1 where  `name` = %s and isDelete = %s '''
''' 更新用户最后登录应用信息 '''
def update_goto_app( name , appCode, ip):
    isdelete = state.Boole['false']
    yz = (appCode, ip, name, isdelete)
    result = mysql.insert_or_update_or_delete(_update_goto_app_sql, yz)
    return 0 == result


_query_user_roles_sql = '''  select ugu.id, ugu.userID, ugu.roleID, ugu.remark, ugu.isDelete, ugu.creater, 
                        ugu.createTime, ugu.lastUpdater, ugu.lastUpdateTime, u.`name` as roleName from sso_user_role as ugu 
                        LEFT JOIN sso_role u on u.id = ugu.roleID 
                        where ugu.userID = %s and  ugu.isDelete = %s and u.status = %s order by ugu.id desc '''
_query_user_roles_col = str_helper.format_str_to_list_filter_empty(
        'id, userID, roleID, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime, roleName', ',')
''' 分页查询用户所属角色 '''
def query_page_user_roles( userID, page = 1, size = 12):
    isdelete = state.Boole['false']
    yz = (userID, isdelete, state.statusActive)
    roles = mysql.find_page(_query_user_roles_sql, yz, _query_user_roles_col, page, size)
    return roles

''' 查询用户所有的角色 '''
def query_all_user_roles( userID):
    isdelete = state.Boole['false']
    yz = (userID, isdelete, state.statusActive)
    roles = mysql.find_all(_query_user_roles_sql, yz, _query_user_roles_col)
    return roles


_bind_group_role_sql = '''  INSERT INTO sso_user_role(userID, roleID, remark, isDelete, creater, 
        createTime, lastUpdater, lastUpdateTime) VALUES(%s, %s, %s, %s, %s, NOW(), %s, NOW()) '''
''' 绑定用户的角色 '''
def bind_user_role( userID, roleID, user):
    roles = query_all_user_roles(userID)
    if roles != None:
        for role in roles:
            if role['roleID'] == roleID:
                return True
    isdelete = state.Boole['false']
    yz = (userID, roleID, '', isdelete, user, user)
    result = mysql.insert_or_update_or_delete(_bind_group_role_sql, yz)
    return 0 == result


_del_user_role_sql = '''  update sso_user_role set isDelete = %s , lastUpdater = %s , lastUpdateTime = now() WHERE id = %s '''
''' 删除用户角色 '''
def del_user_role( id, user):
    isdelete = state.Boole['true']
    yz = (isdelete, user, id)
    result = mysql.insert_or_update_or_delete(_del_user_role_sql, yz)
    return 0 == result

_get_user_role_sql = '''  select id, userID, roleID from sso_user_role WHERE id = %s '''
_get_user_role_col = str_helper.format_str_to_list_filter_empty('id, userID, roleID', ',')
''' 获得用户角色信息 '''
def get_user_role( id):
    yz = (id)
    info = mysql.find_one(_get_user_role_sql, yz, _get_user_role_col)
    return info


''' 查询用户权限 '''
def query_user_app_right( userID, appCode):
    user = query_one(userID)
    if user == None:
        return None
    funcs = func_logic.query_all_by_app(appCode)
    if None == funcs or len(funcs) <= 0:
        return None

    '''  初始化权限  '''
    funcs = role_logic.init_func_right(funcs)
    
    '''  统计绑定的用户组权限  '''
    userGroups = usergroup_logic.query_all_user_groups(userID)        
    if userGroups != None and len(userGroups) > 0:
        for userGroup in userGroups:
            funcs = usergroup_logic.query_user_group_app_right(userGroupID = userGroup['userGroupID'], appCode = appCode, funcs = funcs)
    
    '''  统计绑定的角色权限  '''
    roles = query_all_user_roles(userID)
    if None != roles and len(roles) > 0:
        for role in roles:
            funcs = role_logic.format_role_func_right(appCode = appCode, roleID = role['roleID'], funcs = funcs)
    return funcs



_user_by_name_key = 'soc_api_user_by_name_%s'
''' 根据用户名获取用户信息 '''
def query_user_by_name_cache( name):
    key = _user_by_name_key % name
    user = redis_cache.getObj(key)
    if None == user:
        user = query_one_by_name(name = name)            
        redis_cache.setObj(key = key, val = user, time = config.cache['apiTimeOut'])
    return user

''' 删除用户名获取用户 '''
def _del_user_by_name_cache( name):
    key = _user_by_name_key % name
    redis_cache.delete(key = key)


