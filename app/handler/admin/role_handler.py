#-*- encoding: utf-8 -*-


import tornado.web
from tornado.escape import json_decode, json_encode
import config

from datetime import datetime, timedelta
import admin_base_handler
from common import redis_cache, state, error
from helper import str_helper, http_helper
from logic import role_logic, application_logic, func_logic

class RoleListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.RoleManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config('角色列表')
        role = self.get_args(['id', 'name'], '')
        role['status'] = int(self.get_arg('status', '0'))
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = role_logic.RoleLogic.instance().query_page(id = role['id'], 
                    name = role['name'], status = role['status'], page = ps['page'], size = ps['size'])
        ps['role'] = role
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/role/list.html', **ps)

class RoleAddOrEditHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.RoleManager'
    _right = 0
    def get(self):
        ps = self.get_page_config('创建角色')
        if ps['isedit']:
            self.check_oper_right(right = state.operEdit)
            ps['title'] = self.get_page_title('编辑角色')
            id = int(self.get_arg('id', '0'))
            role = role_logic.RoleLogic.instance().query_one(id)
            if None == role:
                ps['msg'] = state.ResultInfo.get(104002, '')
                ps['gotoUrl'] =  ps['siteDomain'] + 'Admin/Role/List'
                role = {'id':'','name':'','status':1,'remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        else:
            self.check_oper_right(right = state.operAdd)
            role = self.get_args(['id', 'name', 'remark'], '')
            role['status'] = int(self.get_arg('status', '0'))
        ps['role'] = role
        ps = self.format_none_to_empty(ps)
        self.render('admin/role/add_or_edit.html', **ps)

    def post(self):
        ps = self.get_page_config('创建角色')
        if ps['isedit']:
            ps['title'] = self.get_page_title('编辑角色')

        role = self.get_args(['id', 'name', 'remark'], '')
        role['status'] = int(self.get_arg('status', '0'))
        ps['role'] = role
        msg = self.check_str_empty_input(role, ['name'])
        if str_helper.is_null_or_empty(msg) == False:
            ps['msg'] = msg
            ps = self.format_none_to_empty(ps)
            self.render('admin/role/add_or_edit.html', **ps)
            return
        role['user'] = self.get_oper_user()
        
        if ps['isedit']:
            self.check_oper_right(right = state.operEdit)
            try:
                info = role_logic.RoleLogic.instance().update(id = role['id'], name = role['name'], 
                        status = role['status'], remark = role['remark'], user = role['user'])
                if info:
                    self.redirect(ps['siteDomain'] +'Admin/Role/List')
                    return
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        else:
            self.check_oper_right(right = state.operAdd)
            try:
                info = role_logic.RoleLogic.instance().add(name = role['name'], 
                        status = role['status'], remark = role['remark'], user = role['user'])
                if info > 0:
                    self.redirect(ps['siteDomain'] +'Admin/Role/List')
                    return
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        ps = self.format_none_to_empty(ps)
        self.render('admin/role/add_or_edit.html', **ps)



class RoleDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.RoleManager'
    _right = state.operDel
    def post(self):
        id = int(self.get_arg('id', '0'))
        user = self.get_oper_user()
        type = role_logic.RoleLogic.instance().delete(id = id, user = user)
        if type:
            self.out_ok()
        else:
            self.out_fail(code = 101)

class RoleDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.RoleManager'
    _right = state.operView
    def get(self):
        ps = self.get_page_config('角色详情')
        id = int(self.get_arg('id', '0'))
        role = role_logic.RoleLogic.instance().query_one(id)
        if None == role:
            ps['msg'] = state.ResultInfo.get(104002, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/Role/List'
            role = {'id':'','name':'', 'statusname':'','status':1, 'remark':'','creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}        
        ps['role'] = role
        ps = self.format_none_to_empty(ps)
        self.render('admin/role/detail.html', **ps)


class RoleRightHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.RoleManager.RoleBindRightManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config('编辑角色权限')
        ps['roleID'] = int(self.get_arg('roleID', '0'))
        ps['appCode'] = self.get_arg('appCode', '')
        ps['roles'] = []
        ps['apps'] = []
        roles = role_logic.RoleLogic.instance().query_all_by_active()
        if None == roles or len(roles) == 0:
            ps['msg'] = state.ResultInfo.get(104003, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/Role/Add'
            self.render('admin/role/right_edit.html', **ps)
            return
        else:
            if 0 == ps['roleID']:
                ps['roleID'] = roles[0]['id']    
        apps = application_logic.ApplicationLogic.instance().query_all_by_active()
        if None == apps or len(apps) == 0:
            ps['msg'] = state.ResultInfo.get(104003, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/Application/Add'
            self.render('admin/role/right_edit.html', **ps)
            return
        else:
            if '' == ps['appCode']:
                ps['appCode'] = apps[0]['code']
        ps['apps'] = apps
        ps['roles'] = roles
        ps = self.format_none_to_empty(ps)

        funcs = func_logic.FuncLogic.instance().query_all_by_app(ps['appCode'])     #获得应用下的所有功能
        if None != funcs and len(funcs) > 0:
            funcs = role_logic.RoleLogic.instance().init_func_right(funcs)
            funcs = role_logic.RoleLogic.instance().format_role_func_right(appCode = ps['appCode'], roleID = ps['roleID'], funcs = funcs)
        else:
            funcs = []
        ps['funcs'] = funcs
        if self.is_edit():
            self.check_oper_right(right = state.operEdit)
            self.render('admin/role/right_edit.html', **ps)
        else:
            self.check_oper_right(right = state.operView)
            self.render('admin/role/right_detail.html', **ps)

    def post(self):
        self.check_oper_right(right = state.operEdit)
        ps = self.get_page_config('编辑角色权限')
        ps['roleID'] = int(self.get_arg('roleID', '0'))
        ps['appCode'] = self.get_arg('appCode', '')
        funcs = func_logic.FuncLogic.instance().query_all_by_app(ps['appCode'])     #获得应用下的所有功能

        funcs = role_logic.RoleLogic.instance().init_func_right(funcs)
        rights = []

        for func in funcs:      #收集权限数据
            map = {}
            map['funcID'] = func['id']
            r = int(self.get_arg(('right_%d_1' % func['id']), '0'))
            r = r + int(self.get_arg(('right_%d_2' % func['id']), '0'))
            r = r + int(self.get_arg(('right_%d_4' % func['id']), '0'))
            r = r + int(self.get_arg(('right_%d_8' % func['id']), '0'))
            func['right'] = r
            map['right'] = r
            customRight = ''
            if func['customJson'] != None:                
                for c in func['customJson']:
                    cid = self.get_arg(('rightcustom_%d_%s' % (func['id'], c['k'])), '')
                    if cid != '':
                        customRight = customRight + cid + ','
                        c['right'] = True
                    else:
                        c['right'] = False
                if customRight != '':
                    customRight = ',' + customRight
            
            map['customRight'] = customRight
            rights.append(map)

        #保存权限信息
        type = role_logic.RoleLogic.instance().add_right_by_role_app(appCode = ps['appCode'], 
            roleID = ps['roleID'], rights = rights, user = self.get_oper_user())
        
        roles = role_logic.RoleLogic.instance().query_all_by_active()
        apps = application_logic.ApplicationLogic.instance().query_all_by_active()
        ps['apps'] = apps
        ps['roles'] = roles
        ps = self.format_none_to_empty(ps)
        ps['funcs'] = funcs

        if type:
            ps['msg'] = state.ResultInfo.get(0, '')
            ps['gotoUrl'] = ps['siteDomain'] +'Admin/Role/List'
        else:
            ps['msg'] = state.ResultInfo.get(104004, '')
        self.render('admin/role/right_edit.html', **ps)
