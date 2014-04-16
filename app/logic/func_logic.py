#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error


_query_all_by_app_sql = '''  select id, name, code, parentID, path, 
                    sort, customJson from sso_func  where  isDelete = %s   '''    
_query_all_by_app_col = str_helper.format_str_to_list_filter_empty('id, name, code, parentID, path, sort, customJson', ',')
''' 根据appcode查询应用的功能信息 '''
def query_all_by_app(appCode):
    sql = _query_all_by_app_sql
    isdelete = state.Boole['false']
    sql = sql + ' and appCode = %s  order by sort desc'  
    yz = (isdelete, appCode)
    funcs = mysql.find_all(sql, yz, _query_all_by_app_col)
    if funcs == None:
        return []
    return _func_tree(funcs)


_query_sql = '''  select id, appCode, name, code, parentID, path, customJson, 
                    sort, status, remark, isDelete, creater, createTime, 
                    lastUpdater, lastUpdateTime from sso_func  where  isDelete = %s   '''    
_query_col = str_helper.format_str_to_list_filter_empty('id, appCode, name, code, parentID, path, customJson, sort, status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime', ',')
''' 根据path获取功能信息 '''
def query_one_by_path( path):
    sql = _query_sql
    isdelete = state.Boole['false']
    sql = sql + ' and path = %s '        
    yz = (isdelete, path)

    func = mysql.find_one(sql, yz, _query_col)
    return func

''' 根据id获取功能信息 '''
def query_one_by_id( id):
    sql = _query_sql
    isdelete = state.Boole['false']
    sql = sql + ' and id = %s '        
    yz = (isdelete, id)
    func = mysql.find_one(sql, yz, _query_col)
    return func



_add_sql = '''   INSERT INTO sso_func(appCode, name, code, parentID, path, customJson, 
                    sort, status, remark, isDelete, creater, createTime, 
                    lastUpdater, lastUpdateTime)  
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, now())  '''
''' 创建功能 '''
def add(appCode, name, code, parentID, path, customJson,
                    sort, status, remark, user):
    if not _check_customJson(customJson):
        raise error.RightError(code = 102001)
    isdelete = state.Boole['false']
    yz = (appCode, name, code, parentID, path, customJson,
                    sort, status, remark, isdelete, user, user)
    result = mysql.insert_or_update_or_delete(_add_sql, yz, True)
    return result


_update_sql = '''   update sso_func set name = %s, sort = %s, customJson = %s,
                        remark = %s, lastUpdater = %s, 
                        lastUpdateTime = now() where id = %s  '''
''' 更新功能 '''
def update( id, name, sort, customJson, remark, user):
    if not _check_customJson(customJson):
        raise error.RightError(code = 102001)
    yz = (name, sort, customJson, remark, user, id)
    result = mysql.insert_or_update_or_delete(_update_sql, yz)
    return 0 == result


_delete_sql = '''   update sso_func set isDelete = %s, lastUpdater = %s, 
                        lastUpdateTime = now() where id = %s OR path like %s;   '''
''' 删除功能 '''
def delete( id, user):
    isdelete = state.Boole['true']
    func = query_one_by_id(id = id)
    if None == func:
        raise error.RightError(code=102002)
    path = func['path'] + '.%'
    yz = (isdelete, user, id, path)
    result = mysql.insert_or_update_or_delete(_delete_sql, yz)
    return 0 == result

''' 验证功能的自定义json信息 '''
def _check_customJson( customJson):
    if None == customJson or '' == customJson:
        return True
    try:
        ls = str_helper.json_decode(customJson)            
        for m in ls:
            keys = m.keys()
            if ('k' not in keys) or ('v' not in keys) or (not isinstance(m['k'], str) and not isinstance(m['k'], unicode)) or (not str_helper.check_num_abc_port__(m['k'])):
                return False
    except:
        return False
    return True


''' 获取应用的功能树 '''
def _func_tree( funcs):
    ls = []
    headls = []
    maxindex = 1
    for func in funcs:
        func['_dotcount'] = func['path'].count('.')            
        if func['_dotcount'] == 1:
            headls.append(func)
            func['_dotcount'] = 0
        if func['_dotcount'] > maxindex:
            maxindex = func['_dotcount']
    index = 1
    nextindex = 1
    for l in headls:
        ls.append(l)
        path = l['path']
        ll = _func_tree_info(funcs, path, maxindex)
        ls.extend(ll)
        
    #ls = sorted(funcs, key = lambda l:(l['path'],l['path']), reverse = False)
    for l in ls:
        del(l['_dotcount'])
    return ls

''' 获取功能树信息 '''
def _func_tree_info( funcs, path, maxindex):
    ls = []
    nowindex = path.count('.')
    if nowindex >= maxindex:
        return ls
    path = path + '.'
    nowindex = nowindex + 1
    for func in funcs:
        if func['_dotcount'] == 0:
            continue
        if nowindex == func['_dotcount'] and func['path'].startswith(path):
            func['_dotcount'] = 0
            ls.append(func)
            ll = _func_tree_info(funcs, func['path'], maxindex)
            ls.extend(ll)
    return ls
        
        