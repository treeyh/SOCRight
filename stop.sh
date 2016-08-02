#!/bin/sh

#stop admin

killall -9 python-socadmin
sleep 2
ps aux|grep python-socadmin

#stop service
killall -9 python-soc
sleep 2
ps aux|grep python-soc
