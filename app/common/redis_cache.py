#-*- encoding: utf-8 -*-

import config
import redis
from helper import str_helper

_conn = None

_cachekeypre = 'soc_right_user_%s'

def _get_redis():
    global _conn
    if None == _conn:
        _conn = redis.ConnectionPool(host=config.cache['host'], port=config.cache['port'], db = config.cache['db'])        
    return redis.Redis(connection_pool=_conn)

def getStr(key):
    r = _get_redis()
    key = _cachekeypre % key
    return r.get(key)
    

def setStr(key, val, time = 0):
    r = _get_redis()
    key = _cachekeypre % key
    if time <= 0:
        r.set(key, val)
    else:
        r.setex(key,  val, time)

def delete(key):
    r = _get_redis()
    key = _cachekeypre % key
    return r.delete(key)


def getObj(key):
    r = _get_redis()
    key = _cachekeypre % key
    json = r.get(key)
    if None == json:
        return None
    return str_helper.json_decode(json)
    

def setObj(key, val, time = 0):
    if None == val:
        return
    json = str_helper.json_encode(val)
    r = _get_redis()
    key = _cachekeypre % key
    if time <= 0:
        r.set(key, json)
    else:
        r.setex(key,  json, time)


