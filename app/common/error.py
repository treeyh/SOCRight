#-*- encoding: utf-8 -*-

from common import state

class RightError(Exception):
    def __init__(self, value = None, code = 999999):
        if None != value:
            self.msg = '%s,%s' % (state.ResultInfo.get(code, ''), value)
        else:
            self.msg = state.ResultInfo.get(code, '')
        self.code = code

    def __str__(self):
        return repr(self.code + '___' + self.msg)