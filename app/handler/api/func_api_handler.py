#-*- encoding: utf-8 -*-

import tornado.web
#import tornado.escape
from datetime import datetime


import config
from common import state, redis_cache
from helper import str_helper
from handler import base_handler
import api_base_handler
from logic import func_logic, user_logic, oper_log_logic


class FuncAddHandler(api_base_handler.ApiBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.FuncManager'

    def get(self):
        params = self.get_args(['appCode', 'name', 'code', 'parentPath', 'customJson', 'remark', 'user'], '')
        params['sort'] = int(self.get_arg('sort', '0'))
        params['status'] = int(self.get_arg('status', '0'))

        msg = self.check_str_empty_input(params, ['appCode', 'name', 'code', 'parentPath', 'user'])
        if str_helper.is_null_or_empty(msg) == False:
            self.out_fail(code = 1001, msg = msg)
            return

        btype = str_helper.check_num_abc__(params['code'])
        if btype == False:
            self.out_fail(code = 1001, msg = '编号参数只允许输入英文字母、数字和下划线')
            return

        parent = func_logic.query_one_by_path(path = params['parentPath'])
        if None == parent:
            self.out_fail(code = 102004)
            return

        path = parent['path']+'.'+params['code']
        func = func_logic.query_one_by_path(path = path)
        if None != func:
            self.out_fail(code = 102003)
            return

        user = user_logic.query_one_by_name(params['user'])
        if None == user:
            self.out_fail(code = 103002)

        result = func_logic.add(appCode = params['appCode'], name = params['name'], 
            code = params['code'], parentID = parent['id'], path = path, 
            customJson = params['customJson'], sort = params['sort'], 
            status = params['status'], remark = params['remark'], user = params['user'])

        self.out_ok()
        
        self.write_oper_log(action = 'funcCreateInterface', targetType = 3, targetID = str(result), targetName = params['name'], startStatus = '', endStatus= str_helper.json_encode(params), user = user)
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
        