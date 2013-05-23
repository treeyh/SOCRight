#-*- encoding: utf-8 -*-

from datetime import date, datetime, timedelta


def get_now_datestr():
    return datetime.now().strftime('%Y-%m-%d')


def get_now_datestr1(days):
    d = datetime.now() + timedelta(days=days)
    return d.strftime('%Y-%m-%d')

print get_now_datestr1(1)