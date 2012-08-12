#-*- encoding: utf-8 -*-

import urllib2

def get(url, params = {}):
    try:
        c = urllib2.urlopen(url % params)        
        j = c.read()
        return j
    except:
        print 'http helper error!!!url:%s' % (url % params)
        return None