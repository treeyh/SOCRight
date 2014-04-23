#-*- encoding: utf-8 -*-

import urllib
import urllib2
import socket
import sys

def get(url, params = {}):
    try:
        c = urllib2.urlopen(url % params)        
        j = c.read()
        return j
    except:
        print 'http helper error!!!url:%s' % (url % params)
        return None

###GB18030
def http(url, params = {}, method = 'GET', headers = {}, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, htmlEncode = 'UTF-8', exportEncode = 'UTF-8'):
    '''  
        HTTP 模拟请求
        url：请求地址
        params：传入参数，map形式传入
        headers：模拟http头
        method：http请求模式，默认GET
        timeout：超时时间
        htmlEncode：请求内容的编码，默认UTF-8
        exportEncode：输出内容编码，默认UTF-8
    '''
    try:
        req = None
        if 'GET' == method:
            data = urllib.urlencode(params)
            url = '%s?%s' % (url , data)
            req = urllib2.Request(url = url, headers = headers)
        else:
            data = urllib.urlencode(params)
            req = urllib2.Request(url = url, data = data, headers = headers)
        
        c = urllib2.urlopen(req, timeout=timeout).read()
        if htmlEncode != exportEncode:
            c = c.decode(htmlEncode).encode(exportEncode)
        return c
    except:
        print "Unexpected error:", sys.exc_info()
        return None