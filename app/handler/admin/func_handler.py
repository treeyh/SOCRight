#-*- encoding: utf-8 -*-


import tornado.web
from tornado.escape import json_decode, json_encode
import config

from datetime import datetime, timedelta
import admin_base_handler
from common import redis_cache, state, error
from helper import str_helper, http_helper
from logic import application_logic, func_logic




class FuncListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.FuncManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '应用功能列表')
        apps = application_logic.ApplicationLogic.instance().query_all_by_active()
        if None == apps or len(apps) <= 0:
            ps['msg'] = state.ResultInfo.get(101004, '')
            ps['gotoUrl'] = ps['siteDomain'] + 'Admin/Application/Add'
            ps['apps'] = []
            ps['funcs'] = []
            self.render('admin/func/list.html', **ps)
            return
        appCode = self.get_arg('appCode', apps[0]['code'])
        ps['apps'] = apps
        appName = ''
        for app in apps:
            if app['code'] == appCode:
                appName = app['name']
                break
        ps['funcs'] = func_logic.FuncLogic.instance().query_all_by_app(appCode)
        ps['appCode'] = appCode
        self.render('admin/func/list.html', **ps)


class FuncAddOrEditHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.FuncManager'
    _right = 0
    def get(self):
        ps = self.get_page_config(title = '应用功能编辑')
        apps = application_logic.ApplicationLogic.instance().query_all_by_active()
        if None == apps or len(apps) <= 0:
            ps['msg'] = state.ResultInfo.get(101004, '')
            ps['gotoUrl'] = ps['siteDomain'] + 'Admin/Application/Add'
            ps['apps'] = []
            ps['funcs'] = []
            self.render('admin/func/list.html', **ps)
            return

        appCode = self.get_arg('appCode', apps[0]['code'])
        ps['apps'] = apps
        appName = ''
        for app in apps:
            if app['code'] == appCode:
                appName = app['name']
                break
        ps['tree'] = self.get_funcs_tree_by_appCode(appCode, appName)
        ps['appCode'] = appCode
        self.render('admin/func/detail.html', **ps)

    def get_funcs_tree_by_appCode(self, appCode, appName):
        funcs = func_logic.FuncLogic.instance().query_all_by_app(appCode)
        if None == funcs:
            funcs = []
        funcs.insert(0, {'id':0, 'parentID': -1, 'name': appName, 'open': True})
        tree = '['
        t = True
        for func in funcs:
            if t:
                t = False
                tree = '%s{id: %d, pId: %d, name: "%s", open: true}' % (tree, func['id'], func['parentID'], func['name'].replace('"','\\"'))
            else:
                tree = '%s,{id: %d, pId: %d, name: "%s", open: true}' % (tree, func['id'], func['parentID'], func['name'].replace('"','\\"'))
        tree = '%s]' % (tree)
        return tree

    def post(self):
        func = self.get_args(['appCode', 'name', 'code', 'customJson', 'remark'], '')
        func['id'] = int(self.get_arg('id', '0'))
        func['parentID'] = int(self.get_arg('parentID', '0'))
        func['sort'] = int(self.get_arg('sort', '0'))
        
        msg = self.check_str_empty_input(func, ['code', 'name', 'appCode'])
        if str_helper.is_null_or_empty(msg) == False:
            self.out_fail(code = 1001, msg = msg)
            return
        btype = str_helper.check_num_abc__(func['code'])
        if btype == False:
            self.out_fail(code = 1001, msg = '编号参数只允许输入英文字母、数字和下划线')
            return
        func['user'] = self.get_oper_user()
        if func['id'] <= 0:
            self.check_oper_right(right = state.operAdd)
            if func['parentID'] <= 0:
                func['path'] = '%s.%s' % (func['appCode'], func['code'])
            else:
                func['path'] = '%s.%s' % ((func_logic.FuncLogic.instance().query_one_by_id(func['parentID'])).get('path'), func['code'])
            func['status'] = state.Boole['true']

            f = func_logic.FuncLogic.instance().query_one_by_path(path = func['path'])
            if None != f:
                self.out_fail(code = 102003)
                return
            try:
                result = func_logic.FuncLogic.instance().add(appCode = func['appCode'], name = func['name'], code = func['code'], 
                            parentID = func['parentID'], path = func['path'], customJson = func['customJson'], sort = func['sort'], 
                            status = func['status'], remark = func['remark'], user = func['user'])
                nf = func_logic.FuncLogic.instance().query_one_by_path(func['path'])
                self.write_oper_log(action = 'funcCreate', targetType = 3, targetID = str(nf['id']), targetName = nf['name'], startStatus = '', endStatus= str_helper.json_encode(nf))
            except error.RightError as e:
                self.out_fail(code=e.code)
                return
        else:
            self.check_oper_right(right = state.operEdit)
            try:
                of = func_logic.FuncLogic.instance().query_one_by_id(func['id'])
                func_logic.FuncLogic.instance().update(id = func['id'], name = func['name'],sort = func['sort'], 
                                customJson = func['customJson'],remark = func['remark'],user = func['user'])
                nf = func_logic.FuncLogic.instance().query_one_by_id(func['id'])
                self.write_oper_log(action = 'funcEdit', targetType = 3, targetID = str(nf['id']), targetName = nf['name'], startStatus = str_helper.json_encode(of), endStatus= str_helper.json_encode(nf))
            except error.RightError as e:
                self.out_fail(code=e.code)
                return
        self.out_ok()



class FuncDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.FuncManager'
    _right = state.operDel
    def post(self):
        id = int(self.get_arg('id', '0'))

        user = self.get_oper_user()
        try:
            of = func_logic.FuncLogic.instance().query_one_by_id(id)
            type = func_logic.FuncLogic.instance().delete(id = id, user = user)
            if type:
                self.write_oper_log(action = 'funcDelete', targetType = 3, targetID = str(of['id']), targetName = of['name'], startStatus = str_helper.json_encode(of), endStatus= '')
                self.out_ok()
            else:
                self.out_fail(code = 101)
        except error.RightError as e:
            self.out_fail(code=e.code)


class FuncGetHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.FuncManager'
    _right = state.operView
    def get(self):
        id = int(self.get_arg('id', '0'))
        func = func_logic.FuncLogic.instance().query_one_by_id(id)
        if None != func:
            json = str_helper.json_encode(func)
            self.out_ok(data=json)
        else:
            self.out_fail(1002)