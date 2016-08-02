#!/bin/sh


CUR_DIR=$(cd "$(dirname "$0")"; pwd)
PYTHON_BIN=/opt/soft/python/bin

$PYTHON_BIN/python-socadmin $CUR_DIR/app/start.py -port=9801 -log_file_prefix=$CUR_DIR/logs/ssoadmin.log >>$CUR_DIR/logs/ssoadminshell.log 2>&1 &