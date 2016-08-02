#!/bin/sh


CUR_DIR=$(cd "$(dirname "$0")"; pwd)
PYTHON_BIN=/opt/python/bin

$PYTHON_BIN/python-soc $CUR_DIR/app/start.py -port=9901 -log_file_prefix=$CUR_DIR/logs/sso.log >>$CUR_DIR/logs/ssoshell.log 2>&1 &
$PYTHON_BIN/python-soc $CUR_DIR/app/start.py -port=9902 -log_file_prefix=$CUR_DIR/logs/sso.log >>$CUR_DIR/logs/ssoshell.log 2>&1 &
$PYTHON_BIN/python-soc $CUR_DIR/app/start.py -port=9903 -log_file_prefix=$CUR_DIR/logs/sso.log >>$CUR_DIR/logs/ssoshell.log 2>&1 &
$PYTHON_BIN/python-soc $CUR_DIR/app/start.py -port=9904 -log_file_prefix=$CUR_DIR/logs/sso.log >>$CUR_DIR/logs/ssoshell.log 2>&1 &


$PYTHON_BIN/python-socadmin $CUR_DIR/app/start.py -port=9801 -log_file_prefix=$CUR_DIR/logs/ssoadmin.log >>$CUR_DIR/logs/ssoadminshell.log 2>&1 &
$PYTHON_BIN/python-socadmin $CUR_DIR/app/start.py -port=9802 -log_file_prefix=$CUR_DIR/logs/ssoadmin.log >>$CUR_DIR/logs/ssoadminshell.log 2>&1 &
$PYTHON_BIN/python-socadmin $CUR_DIR/app/start.py -port=9803 -log_file_prefix=$CUR_DIR/logs/ssoadmin.log >>$CUR_DIR/logs/ssoadminshell.log 2>&1 &
$PYTHON_BIN/python-socadmin $CUR_DIR/app/start.py -port=9804 -log_file_prefix=$CUR_DIR/logs/ssoadmin.log >>$CUR_DIR/logs/ssoadminshell.log 2>&1 &

ps aux|grep python-soc
