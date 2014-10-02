#-*- encoding: utf-8 -*-

import tornado.web
from datetime import datetime

import config
from common import state, redis_cache, error
from helper import str_helper
from handler import base_handler
from logic import oper_log_logic


class ApiBaseHandler(base_handler.BaseHandler):    
    
    def write_oper_log(self, action, targetType = 0, targetID = '', targetName = '', startStatus = '', endStatus= '', user = None):
        if None == user:
            return
        oper_log_logic.add(operID=user['id'], operUserName=user['name'], operRealName=user['realName'], 
            appCode='SOCRight', funcPath=self._rightKey, action=action, targetType=targetType, 
            targetID=targetID, targetName=targetName, startStatus=startStatus, endStatus=endStatus, operIp=self.get_user_ip())

