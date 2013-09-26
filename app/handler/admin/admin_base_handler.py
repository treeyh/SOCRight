#-*- encoding: utf-8 -*-

import tornado.web
from datetime import datetime

import config
from common import state, redis_cache
from helper import str_helper
from handler import base_handler
from logic import oper_log_logic


class AdminBaseHandler(base_handler.BaseHandler):    
    def get_current_user(self):
        #if not self.current_user:
        uuid = self.get_cookie(config.SOCRightConfig['adminCookieName'])
        if None == uuid:
            return None
        user = redis_cache.getObj(uuid)        
        return user
    
    def is_edit(self):        
        return 'edit' in self.request.path.lower()

    def get_page_config(self, title, refUrl = ''):
        ps = base_handler.BaseHandler.get_page_config(self, title)
        ps['isedit'] = self.is_edit()
        ru = self.get_arg('refUrl', '')
        if None != ru and '' != ru:
            ps['refUrl'] = ru
        else:
            ru = self.request.headers.get('Referer', refUrl)
            if None != ru and '' != ru and '/Admin/Main' not in ru:
                ps['refUrl'] = ru
            else:
                ps['refUrl'] = refUrl
        return ps

    def get_oper_user(self):
        return self.current_user['name']

    def clear_user_info(self):
        uuid = self.get_cookie(config.SOCRightConfig['adminCookieName'])
        if None == uuid:
            return None
        user = redis_cache.delete(uuid)
        self.clear_all_cookies()



class AdminRightBaseHandler(AdminBaseHandler):
    
    _rightKey = ''
    _right = 0

    _resetPwKey = 'ResetPassword'
    _exportUserKey = 'Export'
    _lockUserKey = 'Lock'

    def prepare(self):
        super(AdminRightBaseHandler, self).prepare()
        user = self.current_user
        if None == user:
            ''' 判断用户是否存在,如果不存在,重新登录 '''
            params = {'backUrl':config.urls['adminBackUrl'], 'appCode': config.SOCRightConfig['appCode']}
            url = self.format_url(config.urls['loginUrl'] , params)
            self.redirect(url)
            return
        self.check_oper_right()


    def check_oper_right(self, right = None):
        '''    判断用户权限  '''
        if right == None:
            right = self._right

        if None == self._rightKey or '' == self._rightKey or None == right or 0 == right:
            return
        
        user = self.current_user
        rights = user.get('rights', [])
        type = False
        for r in rights:
            if r.get('path', '') == self._rightKey:                
                if r.get('right', 0) & right == right:
                    type = True
                break
        if not type:
            if self.get_arg('ajax', '') == 'ajax':
                self.out_fail(code = 1004)
                self.finish()
            else:
                self.redirect(config.SOCRightConfig['siteDomain']+'Admin/NotRight')
            return


    def check_oper_right_custom_right(self, rightKey, customRight):
        user = self.current_user
        rights = user.get('rights', [])
        for r in rights:
            if r.get('path', '') != rightKey:
                continue
            crs = r.get('customRight', [])
            for cr in crs:
                if customRight == cr:
                    return True
            return False
        return False

    def write_oper_log(self, action, targetType = 0, targetID = '', targetName = '', startStatus = '', endStatus= ''):
        u = self.current_user
        oper_log_logic.OperLogLogic.instance().add(operID=u['id'], operUserName=u['name'], operRealName=u[
                                                'realName'], appCode='SOCRight', funcPath=self._rightKey, action=action, targetType=targetType, targetID=targetID, targetName=targetName, startStatus=startStatus, endStatus=endStatus, operIp=self.get_user_ip())