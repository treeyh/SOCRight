#!/bin/sh



#python -u /xxx/xxx.pyo 2>&1 1>>/xxx/xxx.log &

/opt/soft/python/bin/python_sso /opt/www/02_SOC/SOCRight/app/start.py -port=9802 -log_file_prefix=/opt/www/02_SOC/SOCRight/logs/sso.log >>/opt/www/02_SOC/SOCRight/logs/sso.log 2>&1  &
