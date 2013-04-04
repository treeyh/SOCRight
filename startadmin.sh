#!/bin/sh



#python -u /xxx/xxx.pyo 2>&1 1>>/xxx/xxx.log &

/opt/soft/python/bin/python_ssoadmin /opt/www/02_SOC/SOCRight/app/start.py -port=9801 -log_file_prefix=/opt/www/02_SOC/SOCRight/logs/ssoadmin.log >>/opt/www/SOCRight/logs/ssoadmin.log 2>&1 &
