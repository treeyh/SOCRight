#-*- encoding: utf-8 -*-

from tornado.escape import url_escape   

from helper import http_helper, str_helper
import config

def _format_url(url, params):
    if '?' in url:
        url = '%s&' % url
    else:
        url = '%s?' % url
    for k in params.keys():
        url = '%s%s=%s&' % (url, k, url_escape(params[k]))
    return url

def _http_get(url, params):
    url = _format_url(url, params)
    json = http_helper.get(url)
    print json
    obj = str_helper.json_decode(json)

    if None == obj or obj['code'] != 0:
        return None
    return obj['data']


def get_login_user(token):
    params = {'token': token}
    url = '%sUser/Get' % (config.urls['socRightApi'])
    obj = _http_get(url, params)
    return obj


def get_users_by_usergroup(userGroupID):
    params = {'userGroupID': str(userGroupID)}
    url = '%sUser/GetByUserGroup' % (config.urls['socRightApi'])
    return _http_get(url, params)


def get_user_by_name(userName):
    params = {'userName': userName}
    url = '%sUser/GetByUserName' % (config.urls['socRightApi'])
    return _http_get(url, params)

