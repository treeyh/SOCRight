#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error

class OperLogLogic():

    def __init__(self):   
        return

    _instance = None
    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance


    

    _query_sql = '''  select id, operID, operUserName, operRealName, appCode, funcPath, 
    						action, targetType, targetID, startStatus, endStatus, operTime 
    						from  sso_oper_log as u where 1 = 1  '''
    _query_col = str_helper.format_str_to_list_filter_empty('id, operID, operUserName, operRealName, appCode, funcPath, action, targetType, targetID, startStatus, endStatus, operTime ', ',')
    def query(self, operID , operUserName, appCode, funcPath, action, beginTime, endTime, page, size):
        sql = self._query_sql
        ps = []
        if None != operID and 0 != operID:
            sql = sql + ' and u.operID = %s '
            ps.append(operID)
        if None != operUserName and '' != operUserName:
            sql = sql + ' and u.operUserName = %s '
            ps.append(operUserName)
        if None != appCode and '' != appCode:
            sql = sql + ' and u.appCode = %s '
            ps.append(appCode)
        if None != funcPath and '' != funcPath:
            sql = sql + ' and u.funcPath = %s '
            ps.append(funcPath)
        if None != action and '' != action:
            sql = sql + ' and u.action = %s '
            ps.append(action)
        if None != beginTime and '' != beginTime:
            sql = sql + ' and u.operTime >= %s '
            ps.append(beginTime)
        if None != endTime and '' != endTime:
            sql = sql + ' and u.operTime <= %s '
            ps.append(endTime)

        yz = tuple(ps)
        sql = sql + ' order by u.id desc '
        logs = mysql.find_page(sql, yz, self._query_col, page, size)
        if None != logs['data']:
            for r in logs['data']:
                r['operTime'] = str(r['operTime'])[0:20]
                r['operTime'] = str(r['operTime'])[0:20]
        return logs


    _add_sql = '''  INSERT INTO(operID, operUserName, operRealName, appCode, funcPath, 
    						action, targetType, targetID, startStatus, endStatus, operTime) 
							VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now() ) '''
    ''' 添加日志 '''
    def add(self, operID, operUserName, operRealName, appCode, funcPath, action, 
    	targetType, targetID, startStatus, endStatus):
        yz = (operID, operUserName, operRealName, appCode, funcPath, action, targetType, targetID, startStatus, endStatus)
        result = mysql.insert_or_update_or_delete(self._add_sql, yz)
        return 0 == result

        
