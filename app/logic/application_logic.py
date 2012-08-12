#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, ssostatus, ssoerror

class ApplicationLogic():

    def __init__(self):   
        return

    _instance = None
    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance



    _query_sql = '''  select code, name, developer, url, status, remark, 
 isDelete, creater, createTime, lastUpdater, lastUpdateTime from sso_application  where  isDelete = %s   '''
    _query_col = str_helper.format_str_to_list_filter_empty('code, name, developer, url, status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime', ',')
    def query_page(self, name = '', code = '', status = 0, page = 1 , size = 12):
        sql = self._query_sql
        isdelete = ssostatus.Boole['false']
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
        apps = mysql.find_page(sql, yz, self._query_col, page, size)
        if None != apps['data']:
            for r in apps['data']:
                r['statusname'] = ssostatus.Status.get(r['status'])
        return apps
 
    def query_one(self, code = ''):
        sql = self._query_sql
        isdelete = ssostatus.Boole['false']
        ps = [isdelete]        
        if '' != code:
            sql = sql + ' and code = %s '
            ps.append(code)
        else:
            return None
        yz = tuple(ps)
        app = mysql.find_one(sql, yz, self._query_col)
        if None != app:
            app['statusname'] = ssostatus.Status.get(app['status'])
        return app


    def query_one_by_name(self, name = ''):
        sql = self._query_sql
        isdelete = ssostatus.Boole['false']
        sql = sql + ' and name = %s '
        yz = (isdelete, name)
        app = mysql.find_one(sql, yz, self._query_col)
        if None != app:
            app['statusname'] = ssostatus.Status.get(app['status'])
        return app

    _query_all_by_active_sql = '''  select code, name from sso_application  where isDelete = %s   '''
    _query_all_by_active_col = str_helper.format_str_to_list_filter_empty('code, name', ',')
    def query_all_by_active(self):
        sql = self._query_all_by_active_sql

        isdelete = ssostatus.Boole['false']
        sql = sql + ' and status = %s order by createTime asc '        
        yz = (isdelete, ssostatus.statusActive)
        apps = mysql.find_all(sql, yz, self._query_all_by_active_col)
        return apps


    _add_sql = '''   INSERT INTO sso_application(code, name, developer, url, status, remark, 
                         isDelete, creater, createTime, lastUpdater, lastUpdateTime)  
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, now(), %s, now())  '''
    def add(self, name, code, developer, url, status, remark, user):
        obj = self.query_one_by_name(name = name)
        if None != obj:
            raise ssoerror.SsoError(code = 101001)
        obj = self.query_one(code = code)
        if None != obj:
            raise ssoerror.SsoError(code = 101005)
            
        isdelete = ssostatus.Boole['false']
        yz = (code, name, developer, url, status, remark, isdelete, user, user)
        result = mysql.insert_or_update_or_delete(self._add_sql, yz)
        return 0 == result


    _update_sql = '''   update sso_application set name = %s, developer = %s, 
                            url = %s, status = %s, remark = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where code = %s  '''
    def update(self, name, code, developer, url, status, remark, user):
        obj = self.query_one_by_name(name = name)
        if None != obj and obj['code'] != str(code):
            raise ssoerror.SsoError(code = 101001)

        isdelete = ssostatus.Boole['false']
        yz = (name, developer, url, status, remark, user, code)
        result = mysql.insert_or_update_or_delete(self._update_sql, yz)
        return 0 == result

    
    _delete_sql = '''   update sso_application set isDelete = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where code = %s  '''
    def delete(self, code, user):
        isdelete = ssostatus.Boole['true']
        yz = (isdelete, user, code)
        result = mysql.insert_or_update_or_delete(self._delete_sql, yz)
        return 0 == result
