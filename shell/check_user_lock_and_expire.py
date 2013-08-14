#-*- encoding: utf-8 -*-


import datetime, calendar  
import sys

sys.path.append('/opt/www/02_SOC/SOCRight/app/')


from helper import str_helper
from logic import user_logic
from common import state, redis_cache, error


def check_user_lock(users, interval):
	return



def check_user_expire(users, interval):
	return

#今天     
def get_today():   
    return datetime.date.today()  

def _get_user_info(page, size):
	userPage = user_logic.UserLogic.instance().query_page(id = '', name = '', realName = '', departmentID = 0, 
                        tel = '', mobile = '', email = '', status = state.statusUserActive, page = page, size = size)
	return userPage


if __name__ == '__main__':
	up = _get_user_info(page = 1, size = 100)

	print up

	print str_helper.date_string_to_datetime(up['data'][0]['endDate'])

	print get_today()