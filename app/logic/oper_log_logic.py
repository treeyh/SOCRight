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
    						from  sso_oper_log  where 1 = 1  '''
    _query_col = '''    '''
    def query(self, operID , operUserName, appCode, funcPath, action, beginTime, endTime):
    	return None


    _add_sql = '''  INSERT INTO(operID, operUserName, operRealName, appCode, funcPath, 
    						action, targetType, targetID, startStatus, endStatus, operTime) 
							VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now() ) '''
    ''' 添加日志 '''
    def add(self, operID, operUserName, operRealName, appCode, funcPath, action, 
    	targetType, targetID, startStatus, endStatus):
        yz = (operID, operUserName, operRealName, appCode, funcPath, action, targetType, targetID, startStatus, endStatus)
        result = mysql.insert_or_update_or_delete(self._add_sql, yz)
        return 0 == result

        