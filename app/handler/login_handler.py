#-*- encoding: utf-8 -*-


import tornado.web
from datetime import datetime, timedelta

from common import redis_cache, state, error
from helper import str_helper
from logic import user_logic, application_logic, oper_log_logic
import config

import base_handler


class LoginHandler(base_handler.BaseHandler):

    def get(self):
        ps = self.get_page_config('用户登录')
        ps = self.get_args(ls=['backUrl', 'appCode'], default='', map=ps)
        user = self.current_user
        if None != user:
            if '' == ps['appCode']:
                self.redirect(ps['serviceSiteDomain'] + 'AppList')
            else:
                backUrl = user_logic.get_goto_user_url(
                    userID=user['id'], appCode=ps['appCode'], ip=self.get_user_ip(), backUrl=ps['backUrl'])
                self.redirect(backUrl)
            return
        self.render('login_bs.html', **ps)

    def post(self):
        ps = self.get_page_config('登录')
        ps = self.get_args(
            ls=['backUrl', 'appCode', 'userName', 'passWord'], default='', map=ps)
        if ps['userName'] == '' or ps['passWord'] == '':
            self.redirect(ps['serviceSiteDomain'] + 'Login?msg=100001')
            return
        user = user_logic.login(
            ps['userName'], ps['passWord'])
        if None == user:
            self.redirect(ps['serviceSiteDomain'] + 'Login?msg=100002')
            return

        uuid = str_helper.get_uuid()
        redis_cache.setObj(uuid, user, config.cache['userTimeOut'])
        ex = ps['now'] + timedelta(seconds=config.cache['userTimeOut'])
        self.clear_all_cookies()
        self.set_cookie(name=config.SOCRightConfig[
                        'rightCookieName'], value=uuid, expires=ex)

        '''  记录日志 '''
        ac = ps['appCode']
        if None == ac or '' == ac:
            ac = 'SOCRight'
        oper_log_logic.add(operID=user['id'], operUserName=user['name'], operRealName=user[
                                                   'realName'], appCode=ac, funcPath='', action='userLogin', targetType=0, targetID='', targetName='', startStatus='', endStatus='', operIp=self.get_user_ip())


        if None != user['loginCount'] and 0 >= user['loginCount'] and 'passwordedit' not in self.request.path.lower():
            params = {'msg': '100003'}
            url = self.format_url(config.SOCRightConfig[
                                  'serviceSiteDomain'] + 'PassWordEdit', params)
            self.redirect(url)
            return

        if ps['appCode'] != '':
            if None == user['loginCount'] or 0 == user['loginCount']:
                self.redirect(ps['serviceSiteDomain'] + 'PassWordEdit?msg=100003&appCode=' +
                              str_helper.url_escape(ps['appCode']) + '&backUrl=' + 
                              str_helper.url_escape(ps['backUrl']))
            return

            backUrl = user_logic.get_goto_user_url(
                userID=user['id'], appCode=ps['appCode'], ip=self.get_user_ip(), backUrl=ps['backUrl'])

            self.redirect(backUrl)
        else:
            self.redirect(ps['serviceSiteDomain'] + 'AppList')


class LogoutHandler(base_handler.BaseHandler):

    def get(self):
        self.clear_user_info()
        self.redirect(config.urls['loginUrl'])


class AppListHandler(base_handler.BaseRightHandler):

    def get(self):
        ps = self.get_page_config('应用集合列表')
        user = self.current_user
        ps['user'] = user
        ps['apps'] = application_logic.query_all_by_active();
        self.render('app_list_bs.html', **ps)


class AppGotoHandler(base_handler.BaseRightHandler):

    def get(self):
        ps = self.get_page_config('')
        ps['appCode'] = self.get_arg('appCode', '')
        user = self.get_current_user()
        if '' == ps['appCode'] or None == user:
            self.redirect(ps['serviceSiteDomain'] + 'AppList')
            return

        gotoUrl = user_logic.get_goto_user_url(
            userID=user['id'], appCode=ps['appCode'], ip=self.get_user_ip(), backUrl='')
        oper_log_logic.add(operID=user['id'], operUserName=user['name'], operRealName=user[
                                                   'realName'], appCode=ps['appCode'], funcPath='', action='userLogin', targetType=0, targetID='', targetName='', startStatus='', endStatus='', operIp=self.get_user_ip())
        self.redirect(gotoUrl)


class PassWordEditHandler(base_handler.BaseRightHandler):

    def get(self):
        ps = self.get_page_config('修改密码')
        ps = self.get_args(
            ls=['oldPassWord', 'newPassWord1', 'newPassWord2'], default='', map=ps)
        user = self.current_user
        ps['user'] = user
        self.render('password_edit_bs.html', **ps)

    def post(self):
        ps = self.get_page_config('修改密码')
        ls = ['oldPassWord', 'newPassWord1', 'newPassWord2']
        ps = self.get_args(ls=ls, default='', map=ps)
        user = self.current_user
        ps['user'] = user

        msg = self.check_str_empty_input(ps, ls)
        if str_helper.is_null_or_empty(msg) == False:
            ps['msg'] = msg
            ps = self.format_none_to_empty(ps)
            self.render('password_edit_bs.html', **ps)
            return

        try:
            type = user_logic.update_password(name = user['name'], oldPassWord = ps['oldPassWord'] , 
                              newPassWord1=ps['newPassWord1'], newPassWord2=ps['newPassWord2'])
            if type:
                if None != user['loginCount'] and 0 >= user['loginCount']:
                    ''' 第一次强制修改密码后更新登录计数  '''
                    user_logic.update_goto_app(
                        user['name'], config.SOCRightConfig['appCode'], ip=self.get_user_ip())
                    oper_log_logic.add(operID=user['id'], operUserName=user['name'], operRealName=user[
                                                               'realName'], appCode='SOCRight', funcPath='', action='userActivate', targetType=0, targetID='', targetName='', startStatus='', endStatus='', operIp=self.get_user_ip())

                self.clear_user_info()
                ps['msg'] = '操作成功'
                ps['gotoUrl'] = ps['serviceSiteDomain'] + 'Login'
            else:
                ps['msg'] = state.ResultInfo.get(101, '')
        except error.RightError as e:
            ps['msg'] = e.msg

        self.render('password_edit_bs.html', **ps)
