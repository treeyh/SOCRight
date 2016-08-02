#-*- encoding: utf-8 -*-

import os

SOCRightConfig = {

    #系统版本号，可以通过该参数reload，js，css资源文件
    'version':'0.9.1',
    #站点名称
    'siteName' : '云海统一权限管理平台',
    #js域名前缀，不需要修改
    'jsDomain' : '/static/',
    #css域名前缀，不需要修改
    'cssDomain' : '/static/',  

    #后台站点的域名，需要根据实际情况修改
    'siteDomain' : 'http://ssoadmin.ejyi.com/',
    #服务站点的域名，需要根据实际情况修改
    'serviceSiteDomain' : 'http://sso.ejyi.com/',
    
    #页面分页每页显示数
    'size' : 15,
    #搜索选择列表分页每页显示数
    'modelSize' : 5,
    #该系统的应用编号，不需要修改
    'appCode' : 'SOCRight',
    #权限服务保存cookie的key
    'rightCookieName' : 'soc_right_user',
    #权限后台保存cookie的key
    'adminCookieName' : 'soc_right_admin_user',

    #系统部署目录，需要根据实际情况修改
    'realPath' : '/opt/web/sso.socsoft.net/',
    #导出用户信息目录，不需要修改
    'exportUserPath' : 'app/static/export/user/',
    #导出操作日志信息目录，不需要修改
    'exportOperLogPath' : 'app/static/export/operlog/',
}

#系统配置目录，不需要修改
urls = {
    'socRightApi' : SOCRightConfig['serviceSiteDomain']+'Api/',
    'adminBackUrl' : SOCRightConfig['siteDomain']+'Admin/Main',
    'loginUrl' : SOCRightConfig['serviceSiteDomain']+'Login',
}

#系统数据库配置，根据实际情况修改
db = {
    'host' : '192.168.36.55',
    'user' : 'root',
    'passwd' : 'fXL2bO$RQgaRS^lH',
    'db' : 'soc_sso_right',
    'charset':'utf8',
    'port':3306,
}


#redis缓存配置，根据实际情况修改
cache = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0,

    #用户信息超时时间，秒
    'userTimeOut' : 86400,
    #authtoken超时时间，秒
    'userRightTimeOut' : 600,
    #authtoken超时时间，秒
    'apiTimeOut' : 3600,
}

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    #系统调试模式，服务器可设置为False
    debug=True,
)


