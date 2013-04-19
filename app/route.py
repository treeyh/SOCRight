#-*- encoding: utf-8 -*-

import os
from handler import login_handler, test_handler
from handler.api import user_api_handler
from handler.admin import main_handler, application_handler, func_handler, user_handler, role_handler, usergroup_handler




'''        路由规则         '''

route = []
route.append((r'^/', login_handler.LoginHandler))       #服务程序需开启这个
route.append((r'^/Login', login_handler.LoginHandler))
route.append((r'^/Logout', login_handler.LogoutHandler))
route.append((r'^/AppList', login_handler.AppListHandler))
route.append((r'^/AppGoto', login_handler.AppGotoHandler))
route.append((r'^/PassWordEdit', login_handler.PassWordEditHandler))


route.append((r'^/Test', test_handler.TestHandler))


route.append((r'^/Api/User/Get', user_api_handler.UserGetInfoHandler))
route.append((r'^/Api/User/GetByUserGroup', user_api_handler.UserByUserGroupHandler))
route.append((r'^/Api/User/GetByUserName', user_api_handler.UserByUserNameHandler))
route.append((r'^/Api/User/GetByUserNames', user_api_handler.UsersByUserNamesHandler))



#route.append((r'^/', main_handler.MainHandler))        #后台程序需开启这个
route.append((r'^/Admin', main_handler.MainHandler))
route.append((r'^/Admin/Main', main_handler.MainHandler))
route.append((r'^/Admin/NotRight', main_handler.NotRightHandler))
route.append((r'^/Admin/Logout', main_handler.LogoutHandler))
route.append((r'^/Admin/Application/List', application_handler.ApplicationListHandler))
route.append((r'^/Admin/Application/Add', application_handler.ApplicationAddOrEditHandler))
route.append((r'^/Admin/Application/Edit', application_handler.ApplicationAddOrEditHandler))
route.append((r'^/Admin/Application/Detail', application_handler.ApplicationDetailHandler))
# route.append((r'^/Admin/Application/Del', application_handler.ApplicationDelHandler))

route.append((r'^/Admin/Func/List', func_handler.FuncListHandler))
route.append((r'^/Admin/Func/Edit', func_handler.FuncAddOrEditHandler))
route.append((r'^/Admin/Func/Get', func_handler.FuncGetHandler))
route.append((r'^/Admin/Func/AddOrUpdate', func_handler.FuncAddOrEditHandler))
route.append((r'^/Admin/Func/Del', func_handler.FuncDelHandler))

route.append((r'^/Admin/User/List', user_handler.UserListHandler))
route.append((r'^/Admin/User/Add', user_handler.UserAddOrEditHandler))
route.append((r'^/Admin/User/Edit', user_handler.UserAddOrEditHandler))
route.append((r'^/Admin/User/Detail', user_handler.UserDetailHandler))
route.append((r'^/Admin/User/Del', user_handler.UserDelHandler))
route.append((r'^/Admin/User/RoleList', user_handler.UserRoleListHandler))
route.append((r'^/Admin/User/RoleBind', user_handler.UserRoleBindHandler))
route.append((r'^/Admin/User/RoleDel', user_handler.UserRoleDelHandler))
route.append((r'^/Admin/User/RightDetail', user_handler.UserRightDetailHandler))
route.append((r'^/Admin/User/GroupList', user_handler.UserUserGroupListHandler))


route.append((r'^/Admin/Role/List', role_handler.RoleListHandler))
route.append((r'^/Admin/Role/Add', role_handler.RoleAddOrEditHandler))
route.append((r'^/Admin/Role/Edit', role_handler.RoleAddOrEditHandler))
route.append((r'^/Admin/Role/Detail', role_handler.RoleDetailHandler))
route.append((r'^/Admin/Role/Del', role_handler.RoleDelHandler))
route.append((r'^/Admin/Role/RightEdit', role_handler.RoleRightHandler))
route.append((r'^/Admin/Role/RightDetail', role_handler.RoleRightHandler))

route.append((r'^/Admin/UserGroup/List', usergroup_handler.UserGroupListHandler))
route.append((r'^/Admin/UserGroup/Add', usergroup_handler.UserGroupAddOrEditHandler))
route.append((r'^/Admin/UserGroup/Edit', usergroup_handler.UserGroupAddOrEditHandler))
route.append((r'^/Admin/UserGroup/Detail', usergroup_handler.UserGroupDetailHandler))
route.append((r'^/Admin/UserGroup/Del', usergroup_handler.UserGroupDelHandler))
route.append((r'^/Admin/UserGroup/UserList', usergroup_handler.UserGroupUserListHandler))
route.append((r'^/Admin/UserGroup/UserBind', usergroup_handler.UserGroupUserBindHandler))
route.append((r'^/Admin/UserGroup/UserDel', usergroup_handler.UserGroupUserDelHandler))
route.append((r'^/Admin/UserGroup/RoleList', usergroup_handler.UserGroupRoleListHandler))
route.append((r'^/Admin/UserGroup/RoleBind', usergroup_handler.UserGroupRoleBindHandler))
route.append((r'^/Admin/UserGroup/RoleDel', usergroup_handler.UserGroupRoleDelHandler))
route.append((r'^/Admin/UserGroup/RightDetail', usergroup_handler.UserGroupRightDetailHandler))


