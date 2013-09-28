#-*- encoding: utf-8 -*-

from common import redis_cache
from helper import str_helper
from logic import user_logic
import tornado.web
import tornado.escape
from tornado.escape import json_decode
from tornado.escape import json_encode
import config

from datetime import datetime
import base_handler


class TestHandler(base_handler.BaseHandler):
    def get(self):

        self.out_ok('','')
    
    def post(self):
        ps = self.get_page_config('登录')
        ps['appcode'] = self.get_arg('appcode', ps['appcode'])
        username = self.get_arg('username', '')
        password = self.get_arg('password', '')        
        if username == '' or password == '':
            self.redirect("/Login?msg=100001")
            return
        user = user_logic.login(username, password, ps['appcode'])
        if None == user:
            self.redirect("/Login?msg=100002")
            return
        uuid = str_helper.get_uuid()
        redis_cache.setObj(uuid, user, config.cache['userTimeOut'])
        self.set_cookie(name = config.SOCRightConfig['cookiename'], value=uuid, expires=config.cache['userTimeOut'])
        self.render("login.html", **ps)
        



