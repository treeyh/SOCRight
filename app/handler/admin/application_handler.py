#-*- encoding: utf-8 -*-


import tornado.web
import tornado.escape
import config

from datetime import datetime, timedelta
import admin_base_handler
from common import redis_cache, state, error, log
from helper import str_helper, http_helper
from logic import application_logic

class ApplicationListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.AppManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config('应用列表')
        app = self.get_args(['code', 'name'], '')
        app['status'] = int(self.get_arg('status', '0'))
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = application_logic.ApplicationLogic.instance().query_page(name = app['name'], 
                        code = app['code'], status= app['status'], page = ps['page'], size = ps['size'])
        ps['app'] = app
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/application/list.html', **ps)

class ApplicationAddOrEditHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.AppManager'
    _right = 0

    def get(self):
        ps = self.get_page_config('创建应用')
        if ps['isedit']:
            self.check_oper_right(right = state.operEdit)

            ps['title'] = self.get_page_title('编辑应用')
            code = self.get_arg('code', '')
            app = application_logic.ApplicationLogic.instance().query_one(code)
            if None == app:
                ps['msg'] = state.ResultInfo.get(1002, '')
                ps['gotoUrl'] = ps['siteDomain'] + 'Admin/Application/List'
                app = {'code':'','name':'','developer':'','url':'','remark':'','status':1,'creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        else:
            self.check_oper_right(right = state.operAdd)
            app = self.get_args(['code', 'name', 'developer', 'url', 'remark'], '')
            app['status'] = int(self.get_arg('status', '0'))        
        ps['app'] = app
        self.render('admin/application/add_or_edit.html', **ps)

    def post(self):
        ps = self.get_page_config('创建应用')
        if ps['isedit']:
            ps['title'] = self.get_page_title('编辑应用')

        app = self.get_args(['code', 'name', 'developer', 'url', 'remark'], '')
        app['status'] = int(self.get_arg('status', '0'))        
        ps['app'] = app        
        msg = self.check_str_empty_input(app, ['code', 'name', 'url'])
        if str_helper.is_null_or_empty(msg) == False:
            ps['msg'] = msg
            self.render('admin/application/add_or_edit.html', **ps)
            return
        codeType = str_helper.check_num_abc__(app['code'])
        if codeType == False:
            ps['msg'] = state.ResultInfo.get(101006, '')
            self.render('admin/application/add_or_edit.html', **ps)
            return
        app['user'] = self.get_oper_user()
        if ps['isedit']:
            self.check_oper_right(right = state.operEdit)
            try:
                info = application_logic.ApplicationLogic.instance().update(name = app['name'], code = app['code'], 
                        developer = app['developer'], url = app['url'], status = app['status'], remark = app['remark'], user = app['user'])
                if info:
                    self.redirect(ps['siteDomain'] + 'Admin/Application/List')
                    return
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        else:
            self.check_oper_right(right = state.operAdd)
            try:
                info = application_logic.ApplicationLogic.instance().add(name = app['name'], code = app['code'], 
                    developer = app['developer'], url = app['url'], status = app['status'], remark = app['remark'], user = app['user'])
                if info:
                    self.redirect(ps['siteDomain'] + 'Admin/Application/List')
                    return
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        ps = self.format_none_to_empty(ps)
        self.render('admin/application/add_or_edit.html', **ps)



class ApplicationDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.AppManager'
    _right = state.operDel
    def post(self):
        code = self.get_arg('code', '')
        user = self.get_oper_user()
        type = application_logic.ApplicationLogic.instance().delete(code = code, user = user)
        if type:
            self.out_ok()
        else:
            self.out_fail(code = 101)

class ApplicationDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.AppManager'
    _right = state.operView
    def get(self):
        ps = self.get_page_config('应用详情')
        code = self.get_arg('code', '')
        app = application_logic.ApplicationLogic.instance().query_one(code)
        if None == app:
            ps['msg'] = state.ResultInfo.get(1002, '')
            ps['gotoUrl'] = ps['siteDomain'] + 'Admin/Application/List'
            app = {'code':'','name':'','developer':'','url':'','remark':'','status':1,'creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        
        ps['app'] = app
        self.render('admin/application/detail.html', **ps)