#!/bin/sh



#python -u /xxx/xxx.pyo 2>&1 1>>/xxx/xxx.log &

/opt/soft/python/bin/python_ssoservice /opt/www/SOCRight/app/start.py -port=9802 -log_file_prefix=/opt/www/SOCRight/logs/ssoservice9802.log >>/opt/www/SOCRight/logs/ssoservice.log 2>&1  &
