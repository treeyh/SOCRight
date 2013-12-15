#!/bin/sh



#python -u /xxx/xxx.pyo 2>&1 1>>/xxx/xxx.log &

#/opt/soft/python/bin/python_ssoadmin /opt/www/02_SOC/SOCRight/app/start.py -port=9801 -log_file_prefix=/opt/www/02_SOC/SOCRight/logs/ssoadmin.log >>/opt/www/02_SOC/SOCRight/logs/ssoadmin.log 2>&1 &


/opt/soft/python/bin/python_socssoadmin /opt/web/sso.socsoft.net/app/start.py -port=9801 -log_file_prefix=/opt/web/sso.socsoft.net/logs/ssoadmin.log >>/opt/web/sso.socsoft.net/logs/ssoadmin.log 2>&1 &
/opt/soft/python/bin/python_socssoadmin /opt/web/sso.socsoft.net/app/start.py -port=9802 -log_file_prefix=/opt/web/sso.socsoft.net/logs/ssoadmin.log >>/opt/web/sso.socsoft.net/logs/ssoadmin.log 2>&1 &
/opt/soft/python/bin/python_socssoadmin /opt/web/sso.socsoft.net/app/start.py -port=9803 -log_file_prefix=/opt/web/sso.socsoft.net/logs/ssoadmin.log >>/opt/web/sso.socsoft.net/logs/ssoadmin.log 2>&1 &
/opt/soft/python/bin/python_socssoadmin /opt/web/sso.socsoft.net/app/start.py -port=9804 -log_file_prefix=/opt/web/sso.socsoft.net/logs/ssoadmin.log >>/opt/web/sso.socsoft.net/logs/ssoadmin.log 2>&1 &
/opt/soft/python/bin/python_socssoadmin /opt/web/sso.socsoft.net/app/start.py -port=9805 -log_file_prefix=/opt/web/sso.socsoft.net/logs/ssoadmin.log >>/opt/web/sso.socsoft.net/logs/ssoadmin.log 2>&1 &
/opt/soft/python/bin/python_socssoadmin /opt/web/sso.socsoft.net/app/start.py -port=9806 -log_file_prefix=/opt/web/sso.socsoft.net/logs/ssoadmin.log >>/opt/web/sso.socsoft.net/logs/ssoadmin.log 2>&1 &
/opt/soft/python/bin/python_socssoadmin /opt/web/sso.socsoft.net/app/start.py -port=9807 -log_file_prefix=/opt/web/sso.socsoft.net/logs/ssoadmin.log >>/opt/web/sso.socsoft.net/logs/ssoadmin.log 2>&1 &
/opt/soft/python/bin/python_socssoadmin /opt/web/sso.socsoft.net/app/start.py -port=9808 -log_file_prefix=/opt/web/sso.socsoft.net/logs/ssoadmin.log >>/opt/web/sso.socsoft.net/logs/ssoadmin.log 2>&1 &
