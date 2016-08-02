#!/bin/sh

killall -9 python-soc
sleep 2
ps aux|grep python-soc

killall -9 python-socadmin

sleep 2
ps aux|grep python-socadmin
