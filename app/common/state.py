#-*- encoding: utf-8 -*-

ResultInfo = {
    0 : 'OK',

    101 : '数据库操作失败',
    
    1001 : '参数缺少或错误',

    1002 : '该对象不存在',
    1003 : '该对象已存在',
    1004 : '无权限执行该操作',


    100001 : '用户名或密码不能为空',
    100002 : '用户名或密码错误，登录失败',
    100003 : '用户首次登录请修改密码',
    
    
    101001 : '应用名称已存在',
    101002 : '该应用不存在',
    101003 : '应用功能还未添加',
    101004 : '暂无可用应用，请先创建',
    101005 : '应用编号已存在',
    101006 : '应用编号只允许输入英文字母、数字和下划线',


    102001 : '功能用户自定义权限json不符合规范，格式为：[{"k":"a1","v":"功能1"},{"k":"b1","v":"功能2"}],"k"只允许输入英文字母、数字、下划线和小数点',
    102002 : '该功能不存在',
    102003 : '该PATH功能已存在',
    102004 : '父功能不存在',    
    102005 : '功能权限信息不能为空',    
    102006 : '功能权限信息参数验证未通过', 
    

    103001 : '用户Email已存在',
    103002 : '该用户不存在',
    103003 : '角色绑定用户需先创建用户',
    103004 : '用户绑定角色失败，请选择角色',
    103005 : '用户绑定角色失败',
    103006 : '该用户绑定的角色不存在',
    103007 : '请先选择用户',
    103008 : '该用户名已存在',
    103009 : '原始密码错误',
    103010 : '两次新密码输入不同',
    103011 : '原始密码与新密码相同',
    103012 : '密码需要至少8位，并且包含字母和数字',

    
    104001 : '角色名称已存在',
    104002 : '该角色不存在',
    104003 : '编辑权限需先添加角色和应用',
    104004 : '保存权限信息失败，请重试，谢谢。',
    

    105001 : '用户组名称已存在',
    105002 : '该用户组不存在',
    105003 : '该用户组绑定用户需先创建用户组',
    105004 : '用户组绑定用户失败，请选择用户',
    105005 : '用户组绑定用户失败',
    105006 : '该用户组绑定的用户不存在',
    105007 : '用户组绑定角色失败，请选择角色',
    105008 : '用户组绑定角色失败',
    105009 : '该用户组绑定的角色不存在',
    105010 : '请先选择用户组',

    106001 : '部门名称已存在',
    106002 : '该部门不存在',
    106003 : '部门功能还未添加',
    106004 : '暂无可用部门，请先创建',

    999999 : '未知错误',
}

Boole = {
    'true' : 1,
    'false' : 2,
}


Status = {
    1 : u'可用',
    2 : u'不可用',
}
UserStatus = {
    1 : u'可用',
    2 : u'不可用',
    3 : u'锁定',
    4 : u'到期',
}

statusUserActive = 1
statusUserLock = 3
statusUserExpire = 4


statusActive = 1


operView = 1
operAdd = 2
operEdit = 4
operDel = 8



logAction={
    'userLogin' : u'用户登录',#1
    'userActivate' : u'用户激活',
    'userCreate' : u'用户管理_创建',
    'userEdit' : u'用户管理_编辑',
    'userDelete' : u'用户管理_删除',
    'userLock' : u'用户管理_锁定',
    'userUnLock' : u'用户管理_解除锁定',
    'userResetPw' : u'用户管理_重置密码',
    'userBindRole' : u'用户管理_绑定角色',
    'userDeleteRole' : u'用户管理_删除绑定角色',
    'userBindGroup' : u'用户管理_绑定用户组',
    'userDeleteGroup' : u'用户管理_删除绑定用户组',
    'userGroupCreate' : u'用户组管理_创建',#6
    'userGroupEdit' : u'用户组管理_编辑',
    'userGroupDelete' : u'用户组管理_删除',
    'userGroupBindUser' : u'用户组管理_绑定用户',
    'userGroupDeleteUser' : u'用户组管理_删除绑定用户',
    'userGroupBindRole' : u'用户组管理_绑定角色',
    'userGroupDeleteRole' : u'用户组管理_删除绑定角色',
    'appCreate' : u'应用管理_创建',#2
    'appEdit' : u'应用管理_编辑',
    #'appDelete' : u'应用管理_删除',
    'funcCreate' : u'功能管理_创建',#3
    'funcCreateInterface' : u'功能管理_通过接口创建',
    'funcEditInterface' : u'功能管理_通过接口编辑',
    'funcEdit' : u'功能管理_编辑',
    'funcDelete' : u'功能管理_删除',
    'roleCreate' : u'角色管理_创建',#5
    'roleEdit' : u'角色管理_编辑',
    'roleDelete' : u'角色管理_删除',
    #'roleBindUserGroup' : u'角色管理_绑定用户组',
    #'roleDeleteUserGroup' : u'角色管理_删除绑定用户组',
    'roleSetRight' : u'角色管理_权限设置',
    'depCreate' : u'部门管理_创建',#4
    'depEdit' : u'部门管理_编辑',
    #'depDelete' : u'部门管理_删除',
}

logAction2=[
    {'k' : 'userLogin' , 'v' : u'用户登录'},#1
    {'k' : 'userActivate' , 'v' : u'用户激活'},
    {'k' : 'userCreate' , 'v' : u'用户管理_创建'},
    {'k' : 'userEdit' , 'v' : u'用户管理_编辑'},
    {'k' : 'userDelete' , 'v' : u'用户管理_删除'},
    {'k' : 'userLock' , 'v' : u'用户管理_锁定'},
    {'k' : 'userUnLock' , 'v' : u'用户管理_解除锁定'},
    {'k' : 'userResetPw' , 'v' : u'用户管理_重置密码'},
    {'k' : 'userBindRole' , 'v' : u'用户管理_绑定角色'},
    {'k' : 'userDeleteRole' , 'v' : u'用户管理_删除绑定角色'},
    {'k' : 'userBindGroup' , 'v' : u'用户管理_绑定用户组'},
    {'k' : 'userDeleteGroup' , 'v' : u'用户管理_删除绑定用户组'},
    {'k' : 'userGroupCreate' , 'v' : u'用户组管理_创建'},#6
    {'k' : 'userGroupEdit' , 'v' : u'用户组管理_编辑'},
    {'k' : 'userGroupDelete' , 'v' : u'用户组管理_删除'},
    {'k' : 'userGroupBindUser' , 'v' : u'用户组管理_绑定用户'},
    {'k' : 'userGroupDeleteUser' , 'v' : u'用户组管理_删除绑定用户'},
    {'k' : 'userGroupBindRole' , 'v' : u'用户组管理_绑定角色'},
    {'k' : 'userGroupDeleteRole' , 'v' : u'用户组管理_删除绑定角色'},
    {'k' : 'appCreate' , 'v' : u'应用管理_创建'},#2
    {'k' : 'appEdit' , 'v' : u'应用管理_编辑'},
    #'appDelete' : u'应用管理_删除',
    {'k' : 'funcCreate' , 'v' : u'功能管理_创建'},#3
    {'k' : 'funcCreateInterface' , 'v' : u'功能管理_通过接口创建'},#3
    {'k' : 'funcEditInterface' , 'v' : u'功能管理_通过接口修改'},#3
    {'k' : 'funcEdit' , 'v' : u'功能管理_编辑'},
    {'k' : 'funcDelete' , 'v' : u'功能管理_删除'},
    {'k' : 'roleCreate' , 'v' : u'角色管理_创建'},#5
    {'k' : 'roleEdit' , 'v' : u'角色管理_编辑'},
    {'k' : 'roleDelete' , 'v' : u'角色管理_删除'},
    {'k' : 'roleUserDelete' , 'v' : u'角色管理_角色用户解除绑定'},
    #'roleBindUserGroup' : u'角色管理_绑定用户组',
    #'roleDeleteUserGroup' : u'角色管理_删除绑定用户组',
    {'k' : 'roleSetRight' , 'v' : u'角色管理_权限设置'},
    {'k' : 'depCreate' , 'v' : u'部门管理_创建'},#4
    {'k' : 'depEdit' , 'v' : u'部门管理_编辑'},
    #'depDelete' : u'部门管理_删除',
]


func_rights_range = [
    '1',
    '2',
    '4',
    '8',
    '16',
    '32',
    '64',
    '128',
    '256',
    '512',
    '1024',
    '2048',
    '4096',
    '8192',
    '16384',
    '32768',
    '65536',
    '131072',
    '262144',
    '524288',
    '1048576',
    '2097152',
    '4194304',
    '8388608',
    '16777216',
    '33554432',
    '67108864',
    '134217728',
    '268435456',
    '536870912'
]