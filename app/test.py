#-*- encoding: utf-8 -*-

import mysql


def readcsv(fileName):
	file_object = open(fileName)
	list_of_all_the_lines = file_object.readlines( )
	file_object.close()
	return list_of_all_the_lines


lines = readcsv('0720bmspay2.csv')

_sql = 'INSERT INTO bmspayinfo(ACCOUNTCODE, USERID, ACCOUNT, EMAIL) values(%s, %s, %s, %s)'

for line in lines:
	ls = line.split(',')	
	ll = []
	for l in ls:
		l = l.replace('\r\n', '')
		l = l[1:-1]
		ll.append(l)
	mysql.insert_or_update_or_delete(sql)

