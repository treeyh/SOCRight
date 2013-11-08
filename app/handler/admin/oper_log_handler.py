#-*- encoding: utf-8 -*-


import tornado.web
from tornado.escape import json_decode, json_encode
import config

from datetime import datetime, timedelta
import admin_base_handler
from common import redis_cache, state, error
from helper import str_helper, http_helper
from logic import role_logic, application_logic, oper_log_logic


class OperLogListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.OperLogManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '操作日志列表')
        ps['ExportType'] = self.check_oper_right_custom_right(self._rightKey, self._exportUserKey)
        operLog = self.get_args(['operUserName', 'action', 'beginTime', 'endTime'], '')
        operLog['operID'] = int(self.get_arg('operID', '0'))
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = oper_log_logic.query_page(operID = operLog['operID'], operUserName = operLog['operUserName'], appCode = '', funcPath = '', action = operLog['action'], operIp = '', beginTime = operLog['beginTime'], endTime = operLog['endTime'], page = ps['page'], size = ps['size'])
        ps['operLog'] = operLog
        ps['actions'] = state.logAction2
        ps['pager'] = self.build_page_html_bs(page=ps['page'], size=ps[
                                           'size'], total=ps['pagedata']['total'], pageTotal=ps['pagedata']['pagetotal'])
        self.render('admin/operlog/list_bs.html', **ps)


class OperLogExportHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.OperLogManager'
    _right = state.operView

    def get(self):
        type = self.check_oper_right_custom_right(self._rightKey, self._exportUserKey)
        if type == False:
            self.redirect(config.SOCRightConfig['siteDomain']+'Admin/NotRight')
            return

        import sys
        reload(sys)                        
        sys.setdefaultencoding('utf-8')   
        ps = self.get_page_config(title = '导出操作日志列表')

        operLog = self.get_args(['operUserName', 'action', 'beginTime', 'endTime'], '')
        operLog['operID'] = int(self.get_arg('operID', '0'))
        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = oper_log_logic.query_page(operID = operLog['operID'], operUserName = operLog['operUserName'], appCode = '', funcPath = '', action = operLog['action'], operIp = '', beginTime = operLog['beginTime'], endTime = operLog['endTime'], page = ps['page'], size = 99999)
        
        #生成excel文件
        logs = ps['pagedata']['data']
        info = u'''<table><tr><td>id</td><td>操作用户ID</td><td>操作用户名</td><td>操作用户姓名</td><td>操作IP</td>
                    <td>操作时间</td><td>应用编号</td><td>操作类型</td><td>操作目标类型</td><td>操作目标ID</td>
                    <td>操作目标名称</td></tr>'''

        for log in logs:
            u = u'''<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>''' % (str(log['id']), log['operID'], log['operUserName'], 
                        log['operRealName'], log['operIp'], str(log['operTime'])[0:-3], log['appCode'], log['actionname'], str(log['targetType']), 
                        log['targetID'], log['targetName'] )
            info = info + u
        info = info + u'</table>'
        fileName = config.SOCRightConfig['exportOperLogPath'] + str_helper.get_now_datestr() +'_'+ str_helper.get_uuid() + '.xls'

        path = config.SOCRightConfig['realPath'] + fileName

        file_object = open(path, 'w')
        file_object.write(info)
        file_object.close( )    
        self.redirect(config.SOCRightConfig['siteDomain']+fileName)