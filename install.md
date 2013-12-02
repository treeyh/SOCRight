# 1 云海统一权限管理系统平【SOCRight】
目前由Tree维护的开源项目:-)，目前支持linux平台，windows平台理论上也支持，但是还没试验过。

## 1.1 安装步骤

### 1.1.1 安装Nginx 1.2.9版本
可以去网上搜索安装教程，不再累述，理论上也支持nginx1.5.x版本，但未实验过，部署目录自定义，Tree自己部署在/opt/soft/nginx/目录下

### 1.1.2 安装Redis 2.6.16版本
可以去网上搜索安装教程，不再累述，理论上也支持redis2.8.x版本，但未实验过，部署目录自定义，Tree自己部署在/opt/soft/redis/目录下

### 1.1.3 安装Python 2.7.x版本
可以去网上搜索安装教程，不再累述，理论上不支持python 3.x版本（:-)），但未实验过，部署目录自定义，Tree自己部署在/opt/soft/python/目录下

### 1.1.4 安装Mysql 5.1.x版本
可以去网上搜索安装教程，不再累述，注意mysql-server和mysql-devel都需要装，Tree自己使用yum安装

### 1.1.5 安装Python扩展，包括：
 - setuptools-0.6c11
 - MySQL-python-1.2.3
 - redis-py
 - Tornado 3.1.1
可以去网上搜索安装教程，不再累述

### 1.1.6 软连接Python，如下：
 - ln -s /opt/soft/python/bin/python /opt/soft/python/bin/python_socssoadmin
 - ln -s /opt/soft/python/bin/python /opt/soft/python/bin/python_socsso

### 1.1.6 修改redis配置，主要有以下两点：
 - 修改为守护进程模式
     - daemonize yes   
 - 注释save操作
     - #save 900 1
     - #save 300 10
     - #save 60 10000


