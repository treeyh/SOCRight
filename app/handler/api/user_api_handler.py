#-*- encoding: utf-8 -*-

import tornado.web
#import tornado.escape
from tornado.escape import json_decode
from tornado.escape import json_encode
from datetime import datetime


import config
from common import ssostatus, redis_cache
from helper import str_helper
from handler import base_handler
from logic import usergroup_logic, user_logic

#{"code":0,"msg":"OK","data":{"id": 1, "tel": "123", "email": "treeyh@126.com", "name": "\u4f59\u6d77"}}
#{"code":0,"msg":"OK"}
#{"code":0,"msg":"OK","data":{"id": 1, "tel": "123", "email": "treeyh@126.com", "name": "\u4f59\u6d77", "rights": [{"id":12, "path":"xx.aa","right":1, "customRight": ",1,2,3,"}, {"id":13, "path":"xx.aa.bb","right":1, "customRight": ""}]}}
class UserGetInfoHandler(base_handler.BaseHandler):    
    def get(self):
        token = self.get_arg('token','')
        if '' == token:
            self.out_fail(code = 1001, msg = 'token')
            return
        user = redis_cache.getStr(token)
        if None == user:
            self.out_ok()
            return
        redis_cache.delete(token)
        self.out_ok(user)
        return
            
class UserByUserGroupHandler(base_handler.BaseHandler):    
    def get(self):
        userGroupID = int(self.get_arg('userGroupID','0'))
        if 0 == userGroupID:
            self.out_fail(code = 1001, msg = 'userGroupID')
            return

        users = usergroup_logic.UserGroupLogic.instance().query_all_group_users(userGroupID = userGroupID)        
        if None == users or len(users) == 0:
            self.out_ok(data = '[]')
            return
        us = []
        for u in users:
            u1 = {'userName':u['userName'], 'userRealName':u['userRealName']}
            us.append(u1)
        json = str_helper.json_encode(us)
        self.out_ok(data = json)
        return


class UserByUserNameHandler(base_handler.BaseHandler):    
    def get(self):
        userName = self.get_arg('userName','')
        if '' == userName:
            self.out_fail(code = 1001, msg = 'userName')
            return

        user = user_logic.UserLogic.instance().query_one_by_name(name = userName)
        if None == users:
            self.out_ok(data = '{}')
            return
        
        json = str_helper.json_encode(user)
        self.out_ok(data = json)
        return



