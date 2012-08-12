#-*- encoding: utf-8 -*-

import os


SOCRightConfig = {
    'version':'3',
    'siteName' : '云海统一权限管理平台',
    'jsDomain' : '/static/',
    'cssDomain' : '/static/',
    'siteDomain' : 'http://ssoadmin.kanchene.com/',
    'serviceSiteDomain' : 'http://ssoservice.kanchene.com/',

    'size' : 15,
    'appCode' : 'SOCRight',
    'rightCookieName' : 'soc_right_user',
    'adminCookieName' : 'soc_right_admin_user',
}

urls = {
    'socRightApi' : SOCRightConfig['serviceSiteDomain']+'Api/',
    'adminBackUrl' : SOCRightConfig['siteDomain']+'Admin/Main',
    'loginUrl' : SOCRightConfig['serviceSiteDomain']+'Login',
}

#db = {
#    'host' : '192.168.99.83',
#    'user' : 'root',
#    'passwd' : 'root123',
#    'db' : 'SocRight',
#    'charset':'utf8',
#}

db = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'passwd' : 'dswybs',
    'db' : 'SOCRight',
    'charset':'utf8',
}


cache = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0,
    'userTimeOut' : 86400,
    'userRightTimeOut' : 600,
}


settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    debug=True,
)


