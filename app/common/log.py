#-*- encoding: utf-8 -*-


from helper import log_helper
import config

_logger = None
def get_logger():
    if None == _logger:
        _logger = log_helper.get_logger(config.log_path)
    return _logger