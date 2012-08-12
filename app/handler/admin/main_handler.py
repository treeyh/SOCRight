#-*- encoding: utf-8 -*-



import tornado.web
import config

from helper import str_helper, http_helper
from datetime import datetime, timedelta
import admin_base_handler
from common import redis_cache, ssostatus
from proxy import soc_right_proxy




class MainHandler(admin_base_handler.AdminBaseHandler):

    _rightKey = config.SOCRightConfig['appCode'] + '.Login'
    _right = ssostatus.operView

    def get(self):
        ps = self.get_page_config('后台')
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
                user = soc_right_proxy.get_login_user(token = ps['token'])
                if None == user or type(user) != dict or user.get('email','') == '':
                    '''  无法获取用户信息，重新登录 '''
                    self.redirect(config.urls['loginUrl'])
                    return
                else:
                    rights = user.get('rights', [])
                    
                    #for right in rights:
                    #    right['']
                uuid = str_helper.get_uuid()
                redis_cache.setObj(uuid, user, config.cache['userTimeOut'])
                ex = ps['now'] + timedelta(seconds=config.cache['userTimeOut'])
                self.set_cookie(name = config.SOCRightConfig['adminCookieName'], value=uuid, expires=ex)
        ps['user'] = user
        
        self.render('admin/main.html', **ps)




class LogoutHandler(admin_base_handler.AdminBaseHandler):
    def get(self):
        self.clear_user_info()
        self.redirect(config.urls['loginUrl'])


class NotRightHandler(admin_base_handler.AdminBaseHandler):
    def get(self):
        ps = self.get_page_config('无该操作权限')
        self.render('admin/not_right.html', **ps)