#-*- encoding: utf-8 -*-

import tornado.web
#import tornado.escape
from datetime import datetime


import config
from common import state, redis_cache
from helper import str_helper
from handler import base_handler
from logic import func_logic


class FuncAddHandler(base_handler.BaseHandler):
    def get(self):
        params = self.get_args(['appCode', 'name', 'code', 'parentID', 'path', 'customJson', 'remark', 'user'], '')
        params['sort'] = int(self.get_arg('sort', '0'))
        params['status'] = int(self.get_arg('status', '0'))
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


class FuncGetByAppCodeHandler(base_handler.BaseHandler):
    def get(self):
        params = self.get_args(['appCode'], '')

        msg = self.check_str_empty_input(params, ['appCode'])
        if str_helper.is_null_or_empty(msg) == False:
            self.out_fail(code = 1001, msg = msg)
            return
        funcs = func_logic.query_all_by_app(appCode = params['appCode'])        
        self.out_ok(funcs)
        return


class FuncEditHandler(base_handler.BaseHandler):
    def post(self):
        func = self.get_args(['appCode', 'name', 'code', 'customJson', 'remark', 'user'], '')
        func['id'] = int(self.get_arg('id', '0'))
        func['parentID'] = int(self.get_arg('parentID', '0'))
        func['sort'] = int(self.get_arg('sort', '0'))
        
        msg = self.check_str_empty_input(func, ['code', 'name', 'appCode', 'user'])
        if str_helper.is_null_or_empty(msg) == False:
            self.out_fail(code = 1001, msg = msg)
            return

        user = func_logic.update(id = id, name = func['name'], sort = func['sort'], customJson = func['sort'], remark = func['sort'], user = func['user'])
        self.out_ok(user)
        return
        