#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error


_query_sql = '''  select code, name, developer, url, status, remark, 
isDelete, creater, createTime, lastUpdater, lastUpdateTime from sso_application  where  isDelete = %s   '''
_query_col = str_helper.format_str_to_list_filter_empty('code, name, developer, url, status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime', ',')
''' 分页查询应用信息 '''
def query_page( name = '', code = '', status = 0, page = 1 , size = 12):        
    sql = _query_sql
    isdelete = state.Boole['false']
    ps = [isdelete]
    if 0 != status:
        sql = sql + ' and status = %s '
        ps.append(status)
    if '' != name:
        sql = sql + ' and name like %s '
        ps.append('%'+name+'%')
    if '' != code:
        sql = sql + ' and code like %s '
        ps.append('%'+code+'%')
    sql = sql + ' order by createTime asc '
    yz = tuple(ps)
    apps = mysql.find_page(sql, yz, _query_col, page, size)
    if None != apps['data']:
        for r in apps['data']:
            r['statusname'] = state.Status.get(r['status'])
    return apps

''' 根据编号查询应用信息 '''
def query_one( code = ''):
    sql = _query_sql
    isdelete = state.Boole['false']
    ps = [isdelete]        
    if '' != code:
        sql = sql + ' and code = %s '
        ps.append(code)
    else:
        return None
    yz = tuple(ps)
    app = mysql.find_one(sql, yz, _query_col)
    if None != app:
        app['statusname'] = state.Status.get(app['status'])
    return app

''' 根据名称查询应用信息 '''
def query_one_by_name( name = ''):
    sql = _query_sql
    isdelete = state.Boole['false']
    sql = sql + ' and name = %s '
    yz = (isdelete, name)
    app = mysql.find_one(sql, yz, _query_col)
    if None != app:
        app['statusname'] = state.Status.get(app['status'])
    return app

_query_all_by_active_sql = '''  select code, name from sso_application  where isDelete = %s   '''
_query_all_by_active_col = str_helper.format_str_to_list_filter_empty('code, name', ',')
''' 查询所有可用的应用 '''
def query_all_by_active():
    sql = _query_all_by_active_sql

    isdelete = state.Boole['false']
    sql = sql + ' and status = %s order by createTime asc '        
    yz = (isdelete, state.statusActive)
    apps = mysql.find_all(sql, yz, _query_all_by_active_col)
    return apps


_add_sql = '''   INSERT INTO sso_application(code, name, developer, url, status, remark, 
                     isDelete, creater, createTime, lastUpdater, lastUpdateTime)  
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, now(), %s, now())  '''
''' 添加应用 '''
def add(name, code, developer, url, status, remark, user):
    obj = query_one_by_name(name = name)
    if None != obj:
        raise error.RightError(code = 101001)
    obj = query_one(code = code)
    if None != obj:
        raise error.RightError(code = 101005)
        
    isdelete = state.Boole['false']
    yz = (code, name, developer, url, status, remark, isdelete, user, user)
    result = mysql.insert_or_update_or_delete(_add_sql, yz)
    return 0 == result


_update_sql = '''   update sso_application set name = %s, developer = %s, 
                        url = %s, status = %s, remark = %s, lastUpdater = %s, 
                        lastUpdateTime = now() where code = %s  '''
''' 更新应用 '''
def update( name, code, developer, url, status, remark, user):
    obj = query_one_by_name(name = name)
    if None != obj and obj['code'] != str(code):
        raise error.RightError(code = 101001)

    isdelete = state.Boole['false']
    yz = (name, developer, url, status, remark, user, code)
    result = mysql.insert_or_update_or_delete(self._update_sql, yz)
    return 0 == result


_delete_sql = '''   update sso_application set isDelete = %s, lastUpdater = %s, 
                        lastUpdateTime = now() where code = %s  '''
''' 删除应用 '''
def delete(code, user):
    isdelete = state.Boole['true']
    yz = (isdelete, user, code)
    result = mysql.insert_or_update_or_delete(_delete_sql, yz)
    return 0 == result
