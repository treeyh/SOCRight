#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error


_query_sql = '''  select  id, `name`, `status`, remark, isDelete, 
                    creater, createTime, lastUpdater, lastUpdateTime  
                    from  sso_department   where  isDelete = %s   '''
_query_col = str_helper.format_str_to_list_filter_empty('id, name, status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime', ',')
''' 分页查询部门信息 '''
def query_page(name = '', status = 0, page = 1 , size = 12):        
    sql = _query_sql
    isdelete = state.Boole['false']
    ps = [isdelete]
    if 0 != status:
        sql = sql + ' and status = %s '
        ps.append(status)
    if '' != name:
        sql = sql + ' and name like %s '
        ps.append('%'+name+'%')

    sql = sql + ' order by createTime asc '
    yz = tuple(ps)
    deps = mysql.find_page(sql, yz, _query_col, page, size)
    if None != deps['data']:
        for r in deps['data']:
            r['statusname'] = state.Status.get(r['status'])
    return deps

''' 根据编号查询部门信息 '''
def query_one(id = 0):
    sql = _query_sql
    isdelete = state.Boole['false']
    ps = [isdelete]        
    if 0 != id:
        sql = sql + ' and id = %s '
        ps.append(id)
    else:
        return None
    yz = tuple(ps)
    dep = mysql.find_one(sql, yz, _query_col)
    if None != dep:
        dep['statusname'] = state.Status.get(dep['status'])
    return dep

''' 根据名称查询部门信息 '''
def query_one_by_name(name = ''):
    sql = _query_sql
    isdelete = state.Boole['false']
    sql = sql + ' and name = %s '
    yz = (isdelete, name)
    dep = mysql.find_one(sql, yz, _query_col)
    if None != dep:
        dep['statusname'] = state.Status.get(dep['status'])
    return dep

_query_all_by_active_sql = '''  select id, name from sso_department  where isDelete = %s   '''
_query_all_by_active_col = str_helper.format_str_to_list_filter_empty('id, name', ',')
''' 查询所有可用的部门 '''
def query_all_by_active():
    sql = _query_all_by_active_sql

    isdelete = state.Boole['false']
    sql = sql + ' and status = %s order by createTime asc '        
    yz = (isdelete, state.statusActive)
    deps = mysql.find_all(sql, yz, _query_all_by_active_col)
    return deps


_add_sql = '''   INSERT INTO sso_department(name, status, remark, 
                     isDelete, creater, createTime, lastUpdater, lastUpdateTime)  
                    VALUES(%s, %s, %s, %s, %s, now(), %s, now())  '''
''' 添加部门 '''
def add( name, status, remark, user):
    obj = query_one_by_name(name = name)
    if None != obj:
        raise error.RightError(code = 106001)
        
    isdelete = state.Boole['false']
    yz = (name, status, remark, isdelete, user, user)
    result = mysql.insert_or_update_or_delete(_add_sql, yz)
    return 0 == result


_update_sql = '''   update sso_department set name = %s, status = %s, 
                        remark = %s, lastUpdater = %s, 
                        lastUpdateTime = now() where id = %s  '''
''' 更新部门 '''
def update(id, name, status, remark, user):
    obj = query_one_by_name(name = name)
    if None != obj and str(obj['id']) != str(id):
        raise error.RightError(code = 106001)

    isdelete = state.Boole['false']
    yz = (name, status, remark, user, id)
    result = mysql.insert_or_update_or_delete(_update_sql, yz)
    return 0 == result


_delete_sql = '''   update sso_department set isDelete = %s, lastUpdater = %s, 
                        lastUpdateTime = now() where id = %s  '''
''' 删除部门 '''
def delete(id, user):
    isdelete = state.Boole['true']
    yz = (isdelete, user, id)
    result = mysql.insert_or_update_or_delete(_delete_sql, yz)
    return 0 == result
