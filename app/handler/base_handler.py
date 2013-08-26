#-*- encoding: utf-8 -*-

import tornado.web
#import tornado.escape
from tornado.escape import url_escape   
from datetime import datetime

import config
from common import state, redis_cache
from helper import str_helper


class BaseHandler(tornado.web.RequestHandler):    
    def get_current_user(self):
        #if not self.current_user:
        uuid = self.get_cookie(config.SOCRightConfig['rightCookieName'])
        if None == uuid:
            return None
        user = redis_cache.getObj(uuid)
        return user

    def clear_user_info(self):
        uuid = self.get_cookie(config.SOCRightConfig['rightCookieName'])
        if None == uuid:
            return None
        user = redis_cache.delete(uuid)
        self.clear_all_cookies()


    def get_page_title(self, title):
        return '%s -- %s' % (title, config.SOCRightConfig['siteName'])

    def get_page_config(self, title):
        ps = config.SOCRightConfig
        ps['title'] = self.get_page_title(title)
        ps['now'] = datetime.now()
        code = int(self.get_arg('msg', '0'))
        ps['gotoUrl'] = ''
        ps['goLevel'] = ''
        if code > 0:
            ps['msg'] = state.ResultInfo.get(code, '')
        else:
            ps['msg'] = ''
        return ps

    def get_ok_and_back_params(self, ps):
        ps['msg'] = state.ResultInfo.get(0, '')
        ps['goLevel'] = '-2'
        return ps

    def get_header(self, name, default=None): 
         return self._headers.get(name, default)

    def get_arg(self, key, default=None,strip=True):
        val = self.get_argument(key, default, strip)
        if val != None and isinstance(val, unicode):
            val = val.encode('utf-8')
        return val


    def get_args(self, ls=[], default=None, map = {}):
        for l in ls:
            map[l] = self.get_arg(l, default)
        return map

    def out_fail(self, code, msg = None, jsoncallback= None):
        if None != msg and '' != msg:
            msg = '%s,%s' % (state.ResultInfo.get(code, ''), msg)
        else:
            msg = state.ResultInfo.get(code, '')
        j = '{"code":%d,"msg":"%s"}' % (code, msg.replace('"', '\\"'))
        if jsoncallback == None or jsoncallback == '':
            self.write(j)
        else:
            self.write('%s(%s)' % (jsoncallback, j))

    def out_ok(self, data=None, jsoncallback = None):
        if data == None or data == '':
            j = '{"code":0,"msg":"OK"}'
        else:
            j = '{"code":0,"msg":"OK","data":%s}' % data
        if jsoncallback == None or jsoncallback == '':
            self.write(j)
        else:
            self.write('%s(%s)' % (jsoncallback, j))

    def check_str_empty_input(self, map = {}, ls = []):
        error = ''
        for l in ls:
            if str_helper.is_null_or_empty(map[l]):
                error = '%s %s,' % (error, l)
        if str_helper.is_null_or_empty(error) == False:
            error = error + state.ResultInfo.get(1001, '')
        return error


    def format_none_to_empty(self, obj):
        if isinstance(obj, dict):
            for key in obj.keys():
                if isinstance(obj[key], dict) or isinstance(obj[key], list):
                    self.format_none_to_empty(obj[key])
                elif obj[key] == None:
                    obj[key] = ''
        elif isinstance(obj, list):
            for key in obj:
                if isinstance(key, dict) or isinstance(key, list):
                    self.format_none_to_empty(key)
                elif key == None:
                    key = ''
        return obj


    def get_user_ip(self):
        ip = self.request.headers.get('X-Real-Ip', '127.0.0.1')
        if ip == '127.0.0.1':
            ip = self.request.headers.get('X-Forwarded-For', '127.0.0.1')
        if ip == '127.0.0.1':
            ip = self.request.headers.get('HTTP_X_FORWARDED_FOR', '127.0.0.1')
        ip = ip.split(',')
        return ip[0]



    def format_url(self, url, params):
        if '?' in url:
            url = '%s&' % url
        else:
            url = '%s?' % url
        for k in params.keys():
            url = '%s%s=%s&' % (url, k, url_escape(params[k]))
        return url

    def format_page_url(self):
        url = self.request.uri
        p = '&page='
        q = '?page='
        if p in url:
            d = url[0: url.find(p)].strip()
            b = url[url.find(p)+len(p) : -1]
            if b.find('&') >= 0:
                b = b[b.find('&'):-1].strip()
            else:
                b = ''
            url = d + b
        elif q in url:
            d = url[0: url.find(q)].strip()
            b = url[url.find(q)+len(q) : -1]
            if b.find('&') >= 0:
                b = b[b.find('&')+1:-1].strip()
            else:
                b = ''
            url = d + '?' + b
        else:
            url = url.strip()
        if '?' in url:
            url = url + '&page='
        else:
            url = url + '?page='
        return url
    
    def get_page_pagearea(self, page, pageTotal):
        count = 7
        numArea = []
        middleNum = (count / 2) + 1      
        if page <= middleNum:    
            for i in range(1, count+1):
                if i > pageTotal: break;
                numArea.append(i)
        elif (page >= (pageTotal - count + middleNum)):
            start = 1
            if start > (pageTotal - count + start):
                start = start - pageTotal + count
            for i in range(start, count+start):
                index = pageTotal - count + i
                if index > pageTotal: break;
                numArea.append(index)
        else:
            for i in range(1, count+1):
                index = page - middleNum + i
                if index > pageTotal: break;
                numArea.append(index)
        return numArea

    
    def build_page_html(self, page, size, total, pageTotal):
        url = self.format_page_url()
        pageArea = self.get_page_pagearea(page, pageTotal)
        html = '<div style="margin: auto; margin-top: 3px; width: 99%; height:22px; line-height:22px; border: dashed #ccc 1px; text-align: right; font-size: 12px;">'
        html = '%s<label style="margin-right: 20px;">共%d条记录&nbsp;&nbsp;分%d页&nbsp;&nbsp;每页%d条记录</label>' % (html, total, pageTotal, total)

        if len(pageArea) > 0:
            if 1 < page:
                html = '%s<a href="%s1" style="margin-right: 5px;" title="转到第一页">第一页</a>' % (html , url)
                pagepre = page - 1
                html = '%s<a href="%s%d" style="margin-right: 5px;" title="转到上一页">上一页</a>' % (html, url, pagepre)
                if 1 < pageArea[0]:
                    pagepre = pageArea[0] - 1
                    html = '%s<a href="%s%d" title="转到第%d页" style="margin-right: 5px;">....</a>' % (html, url, pagepre, pagepre)
            else:
                html = '%s<a disabled style="margin-right: 5px;">第一页</a><a disabled style="margin-right: 5px;">上一页</a>' % (html)

            for i in pageArea:
                if i == page:
                    html = '%s<label style="font-weight: Bold; color: red; margin-right: 5px;">[%d]</label>' % (html, i)
                else:
                    html = '%s<a style="margin-right: 5px;" title="转到第%d页" href="%s%d">[%d]</a>' % (html, i, url, i, i)

            if pageTotal > page and pageTotal > 0:
                next = pageArea[len(pageArea)-1] + 1
                if pageTotal >= next:
                    html = '%s<a href="%s%d" title="转到第%d页" style="margin-right: 5px;">....</a>' % (html, url, next, next)
                next = page + 1
                html = '%s<a href="%s%d" style="margin-right: 5px;" title="转到下一页">下一页</a>' % (html, url, next)
                html = '%s<a href="%s%d" style="margin-right: 20px;" title="转到最末页">最末页</a>' % (html, url, pageTotal)
            else:
                html = '%s<a disabled style="margin-right: 5px;" title="转到下一页">下一页</a><a disabled style="margin-right: 20px;" title="转到最末页">最末页</a>' % (html)
        else:
            html = '%s<a disabled style="margin-right: 5px;">第一页</a><a disabled style="margin-right: 5px;">上一页</a>' % (html)
            html = '%s<a disabled style="margin-right: 5px;" title="转到下一页">下一页</a><a disabled style="margin-right: 20px;" title="转到最末页">最末页</a>' % (html)

        html = '%s跳转第<input type="text" value="%d" id="btGoToPage" style="margin-left:5px; width:20px;" />页<input type="button" value="Go" style="margin-left:10px;margin-right: 20px;cursor:pointer;" onclick="Common.goToPage(\'%s\', %d)" />' % (html, page, url, pageTotal)

        html = '%s</div>' % html
        return html



class BaseRightHandler(BaseHandler):
    
    _rightKey = ''
    _right = 0

    def prepare(self):
        super(BaseRightHandler, self).prepare()
        user = self.current_user
        if None == user:
            ''' 判断用户是否存在,如果不存在,重新登录 '''
            params = {'backUrl':config.urls['adminBackUrl'], 'appCode': config.SOCRightConfig['appCode']}
            url = self.format_url(config.urls['loginUrl'] , params)
            self.redirect(url)
            return
            
        if None != user['loginCount'] and 0 >= user['loginCount'] and 'passwordedit' not in self.request.path.lower():
            params = {'msg': '100003'}
            url = self.format_url(config.SOCRightConfig['serviceSiteDomain'] + 'PassWordEdit' , params)
            self.redirect(url)
            return