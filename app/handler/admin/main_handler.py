#-*- encoding: utf-8 -*-



import tornado.web
import config

from helper import str_helper, http_helper
from datetime import datetime, timedelta
import admin_base_handler
from common import redis_cache, state
from proxy import soc_right_proxy




class MainHandler(admin_base_handler.AdminBaseHandler):

    _rightKey = config.SOCRightConfig['appCode'] + '.Login'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '后台')
        token = self.get_args(['token'], '')
        ps['token'] = token['token']
        user = self.current_user
        if None == user:
            ''' 判断用户是否存在，如果不存在，判断token重新登录 '''
            if '' == ps['token']:
                params = {'backUrl':config.urls['adminBackUrl'], 'appCode': ps['appCode']}
                url = self.format_url(config.urls['loginUrl'] , params)
                self.redirect(url)
                return
            else:                
                user = self.get_user_info_by_token(token = ps['token'])
        elif ps['token'] != '' and user.get('loginToken', '') != ps['token']:
            '''  用户登录token不等于传入token，需要重新登录  '''
            user = self.get_user_info_by_token(token = ps['token'])

        ps['user'] = user
        self.check_oper_right(user = user)

        self.render('admin/main_bs.html', **ps)

    def get_user_info_by_token(self , token):
        user = soc_right_proxy.get_login_user(token = token)
        if None == user or type(user) != dict or user.get('email','') == '':
            '''  无法获取用户信息，重新登录 '''
            self.redirect(config.urls['loginUrl'])
            return
        else:
            rights = user.get('rights', [])
        user['loginToken'] = token
        uuid = str_helper.get_uuid()
        redis_cache.setObj(uuid, user, config.cache['userTimeOut'])
        ex = datetime.now() + timedelta(seconds=config.cache['userTimeOut'])
        self.set_cookie(name = config.SOCRightConfig['adminCookieName'], value=uuid, expires=ex)
        return user

    def check_oper_right(self, user):
        '''    判断用户权限  '''
        right = self._right

        if None == self._rightKey or '' == self._rightKey or None == right or 0 == right:
            return
        
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




class LogoutHandler(admin_base_handler.AdminBaseHandler):
    def get(self):
        self.clear_user_info()
        self.redirect(config.urls['loginUrl'])


class NotRightHandler(admin_base_handler.AdminBaseHandler):
    def get(self):
        ps = self.get_page_config(title = '无该操作权限')
        self.render('admin/not_right_bs.html', **ps)


class IndexHandler(admin_base_handler.AdminBaseHandler):
    _rightKey = config.SOCRightConfig['appCode'] + '.Login'
    _right = state.operView

    def get(self):
        ps = self.get_page_config(title = '欢迎访问')
        ps['user'] = self.current_user
        self.render('admin/index_bs.html', **ps)