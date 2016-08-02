#!/bin/sh


CUR_DIR=$(cd "$(dirname "$0")"; pwd)
PYTHON_BIN=/opt/python/bin

#start service
$PYTHON_BIN/python-soc $CUR_DIR/app/start.py -port=9901 -log_file_prefix=$CUR_DIR/logs/sso9901.log -service_log_file=$CUR_DIR/logs/sso.log >>$CUR_DIR/logs/ssoshell.log 2>&1 &
$PYTHON_BIN/python-soc $CUR_DIR/app/start.py -port=9902 -log_file_prefix=$CUR_DIR/logs/sso9902.log -service_log_file=$CUR_DIR/logs/sso.log >>$CUR_DIR/logs/ssoshell.log 2>&1 &
$PYTHON_BIN/python-soc $CUR_DIR/app/start.py -port=9903 -log_file_prefix=$CUR_DIR/logs/sso9903.log -service_log_file=$CUR_DIR/logs/sso.log >>$CUR_DIR/logs/ssoshell.log 2>&1 &
$PYTHON_BIN/python-soc $CUR_DIR/app/start.py -port=9904 -log_file_prefix=$CUR_DIR/logs/sso9904.log -service_log_file=$CUR_DIR/logs/sso.log >>$CUR_DIR/logs/ssoshell.log 2>&1 &

#start admin
$PYTHON_BIN/python-socadmin $CUR_DIR/app/start.py -port=9801 -log_file_prefix=$CUR_DIR/logs/ssoadmin9801.log -service_log_file=$CUR_DIR/logs/ssoadmin.log >>$CUR_DIR/logs/ssoadminshell.log 2>&1 &
$PYTHON_BIN/python-socadmin $CUR_DIR/app/start.py -port=9802 -log_file_prefix=$CUR_DIR/logs/ssoadmin9802.log -service_log_file=$CUR_DIR/logs/ssoadmin.log >>$CUR_DIR/logs/ssoadminshell.log 2>&1 &
$PYTHON_BIN/python-socadmin $CUR_DIR/app/start.py -port=9803 -log_file_prefix=$CUR_DIR/logs/ssoadmin9803.log -service_log_file=$CUR_DIR/logs/ssoadmin.log >>$CUR_DIR/logs/ssoadminshell.log 2>&1 &
$PYTHON_BIN/python-socadmin $CUR_DIR/app/start.py -port=9804 -log_file_prefix=$CUR_DIR/logs/ssoadmin9804.log -service_log_file=$CUR_DIR/logs/ssoadmin.log >>$CUR_DIR/logs/ssoadminshell.log 2>&1 &

sleep 2

ps aux|grep python-soc
