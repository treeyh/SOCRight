#-*- encoding: utf-8 -*-


import tornado.web
import tornado.escape
import config

from datetime import datetime, timedelta
import admin_base_handler
from common import redis_cache, state, error, log
from helper import str_helper, http_helper
from logic import department_logic

class DepartmentListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.DepartmentManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '部门列表')
        dep = {}
        dep['name'] = self.get_arg('name', '')
        dep['status'] = int(self.get_arg('status', '0'))
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = department_logic.query_page(name = dep['name'], 
                        status= dep['status'], page = ps['page'], size = ps['size'])
        ps['dep'] = dep
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/department/list.html', **ps)

class DepartmentAddOrEditHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.DepartmentManager'
    _right = state.operAdd

    def get(self):
        ps = self.get_page_config(title = '创建部门', refUrl = config.SOCRightConfig['siteDomain'] + 'Admin/Department/List')
        if ps['isedit']:
            self.check_oper_right(right = state.operEdit)

            ps['title'] = self.get_page_title('编辑部门')
            id = int(self.get_arg('id', '0'))
            dep = department_logic.query_one(id = id)
            if None == dep:
                ps['msg'] = state.ResultInfo.get(1002, '')
                dep = {'id':'','name':'','remark':'','status':1,'creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        else:
            self.check_oper_right(right = state.operAdd)
            dep = self.get_args(['name', 'remark'], '')
            dep['status'] = int(self.get_arg('status', '0'))        
        ps['dep'] = dep
        self.render('admin/department/add_or_edit.html', **ps)

    def post(self):
        ps = self.get_page_config(title = '创建部门')        
        if ps['isedit']:
            ps['title'] = self.get_page_title('编辑部门')
        
        dep = self.get_args(['name', 'remark'], '')
        dep['status'] = int(self.get_arg('status', '0'))
        dep['id'] = int(self.get_arg('id', '0'))
        ps['dep'] = dep        
        msg = self.check_str_empty_input(dep, ['name'])
        if str_helper.is_null_or_empty(msg) == False:
            ps['msg'] = msg
            self.render('admin/department/add_or_edit.html', **ps)
            return
        dep['user'] = self.get_oper_user()
        if ps['isedit']:
            self.check_oper_right(right = state.operEdit)

            try:
                od = department_logic.query_one(dep['id'])
                info = department_logic.update(id = dep['id'], name = dep['name'], 
                    status = dep['status'], remark = dep['remark'], user = dep['user'])
                
                if info:
                    nd = department_logic.query_one(dep['id'])
                    self.write_oper_log(action = 'depEdit', targetType = 4, targetID = str(nd['id']), targetName = nd['name'], startStatus = str_helper.json_encode(od), endStatus= str_helper.json_encode(nd))
                    ps = self.get_ok_and_back_params(ps = ps, refUrl = ps['refUrl'])
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        else:
            self.check_oper_right(right = state.operAdd)
            try:
                info = department_logic.add(name = dep['name'],
                        status = dep['status'], remark = dep['remark'], user = dep['user'])
                if info:
                    nd = department_logic.query_one_by_name(dep['name'])
                    self.write_oper_log(action = 'depCreate', targetType = 4, targetID = str(nd['id']), targetName = nd['name'], startStatus = '', endStatus= str_helper.json_encode(nd))
                    ps = self.get_ok_and_back_params(ps = ps, refUrl = ps['refUrl'])
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.RightError as e:
                ps['msg'] = e.msg
        ps = self.format_none_to_empty(ps)
        self.render('admin/department/add_or_edit.html', **ps)



class DepartmentDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.DepartmentManager'
    _right = state.operDel
    def post(self):
        code = self.get_arg('code', '')
        user = self.get_oper_user()
        type = application_logic.delete(code = code, user = user)
        if type:
            self.out_ok()
        else:
            self.out_fail(code = 101)

class DepartmentDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.DepartmentManager'
    _right = state.operView
    def get(self):
        ps = self.get_page_config(title = '部门详情')
        id = int(self.get_arg('id', '0'))
        dep = department_logic.query_one(id = id)
        if None == dep:
            ps['msg'] = state.ResultInfo.get(1002, '')
            ps['gotoUrl'] = ps['siteDomain'] + 'Admin/Department/List'
            app = {'name':'','remark':'','status':1,'creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        
        ps['dep'] = dep
        self.render('admin/department/detail.html', **ps)