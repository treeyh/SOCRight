#-*- encoding: utf-8 -*-

#  计划任务：1、N天未登录锁定账号；2、账号超过使用期限锁定账号；
#
#
#




import datetime, calendar  
import sys
import os

path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(path + '/../app/')

#设置多少天未登录即锁定账号
lockDay = 30


from helper import str_helper
from logic import user_logic
from common import state, redis_cache, error



#今天     
def get_today():   
    return datetime.datetime.today()


def _get_user_info(page, size):
	userPage = user_logic.query_page(id = '', name = '', realName = '', departmentID = 0, 
                        tel = '', mobile = '', email = '', status = state.statusUserActive, page = page, size = size)
	return userPage




if __name__ == '__main__':
	today = get_today()	

	for p in range(1, 9999):

		up = _get_user_info(page = p, size = 1000)
		print up
		if 0 == len(up['data']):
			break
		for user in up['data']:
			endDate = str_helper.date_string_to_datetime(user['endDate'])			

			'''  验证是否超过截止日期  begin '''			
			inv = endDate - today
			if inv.days < 0:
				user_logic.update_status(id = user['id'], status = state.statusUserExpire, user = 'sys')


			'''  验证是否登录超过30天  end '''
			lastLoginTime = user.get('lastLoginTime', None)
			if None == lastLoginTime or '' == lastLoginTime:
				lastLoginTime = user['lastUpdateTime']
			inv2 = today - lastLoginTime
			print '%s--%s--%d' % (user['name'], str(lastLoginTime) ,inv2.days)
			if inv2.days > lockDay:
				user_logic.update_status(id = user['id'], status = state.statusUserLock, user = 'sys')




	


	

	