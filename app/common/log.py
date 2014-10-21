#-*- encoding: utf-8 -*-

import logging
import config

from helper import log_helper


_logFilePath = '%s%s' % (config.SOCRightConfig['realPath'], config.SOCRightConfig['sysLogFile'])

def info(log):
    log_helper.get_logger(_logFilePath).info(log)