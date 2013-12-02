#!/bin/sh



#python -u /xxx/xxx.pyo 2>&1 1>>/xxx/xxx.log &

#/opt/soft/python/bin/python_sso /opt/www/02_SOC/SOCRight/app/start.py -port=9802 -log_file_prefix=/opt/www/02_SOC/SOCRight/logs/sso.log >>/opt/www/02_SOC/SOCRight/logs/sso.log 2>&1  &



/opt/soft/python/bin/python_socsso /opt/web/sso.eeshou.com/app/start.py -port=9811 -log_file_prefix=/opt/web/sso.eeshou.com/logs/sso.log >>/opt/web/sso.eeshou.com/logs/sso.log 2>&1 &
/opt/soft/python/bin/python_socsso /opt/web/sso.eeshou.com/app/start.py -port=9812 -log_file_prefix=/opt/web/sso.eeshou.com/logs/sso.log >>/opt/web/sso.eeshou.com/logs/sso.log 2>&1 &
/opt/soft/python/bin/python_socsso /opt/web/sso.eeshou.com/app/start.py -port=9813 -log_file_prefix=/opt/web/sso.eeshou.com/logs/sso.log >>/opt/web/sso.eeshou.com/logs/sso.log 2>&1 &
/opt/soft/python/bin/python_socsso /opt/web/sso.eeshou.com/app/start.py -port=9814 -log_file_prefix=/opt/web/sso.eeshou.com/logs/sso.log >>/opt/web/sso.eeshou.com/logs/sso.log 2>&1 &
/opt/soft/python/bin/python_socsso /opt/web/sso.eeshou.com/app/start.py -port=9815 -log_file_prefix=/opt/web/sso.eeshou.com/logs/sso.log >>/opt/web/sso.eeshou.com/logs/sso.log 2>&1 &
/opt/soft/python/bin/python_socsso /opt/web/sso.eeshou.com/app/start.py -port=9816 -log_file_prefix=/opt/web/sso.eeshou.com/logs/sso.log >>/opt/web/sso.eeshou.com/logs/sso.log 2>&1 &
/opt/soft/python/bin/python_socsso /opt/web/sso.eeshou.com/app/start.py -port=9817 -log_file_prefix=/opt/web/sso.eeshou.com/logs/sso.log >>/opt/web/sso.eeshou.com/logs/sso.log 2>&1 &
/opt/soft/python/bin/python_socsso /opt/web/sso.eeshou.com/app/start.py -port=9818 -log_file_prefix=/opt/web/sso.eeshou.com/logs/sso.log >>/opt/web/sso.eeshou.com/logs/sso.log 2>&1 &
