#!/bin/sh


CUR_DIR=$(cd "$(dirname "$0")"; pwd)
PYTHON_BIN=/opt/soft/python/bin

$PYTHON_BIN/python_soc $CUR_DIR/app/start.py -port=9802 -log_file_prefix=$CUR_DIR/logs/sso.log >>$CUR_DIR/logs/ssoshell.log 2>&1 &
