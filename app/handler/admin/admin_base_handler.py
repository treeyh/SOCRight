#-*- encoding: utf-8 -*-

import tornado.web
from datetime import datetime

import config
from common import ssostatus, redis_cache
from helper import str_helper
from handler import base_handler


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

    def get_page_config(self, title):
        ps = base_handler.BaseHandler.get_page_config(self, title)
        ps['isedit'] = self.is_edit()
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

    def prepare(self):
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