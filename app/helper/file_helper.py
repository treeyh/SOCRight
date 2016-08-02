#-*- encoding: utf-8 -*-

import os
import codecs
from hashlib import md5

import shutil


# # http://stackoverflow.com/questions/847850/cross-platform-way-of-getting-temp-directory-in-python
# 'filename': os.path.join(tempfile.gettempdir(), 'glances.log')

def exists_file(filePath):
    ''' 
        判断文件是否存在 
        filePath:目录路径
    '''
    return os.path.exists(filePath)

def is_file(path):
    ''' 
        返回路径是否为文件
    '''
    return os.path.isfile(path)

def remove_file(filePath):
    ''' 
        删除文件
    '''
    os.remove(filePath)

def remove_folder(path):    
    ''' 
        删除目录
    '''
    # os.rmdir(path)
    shutil.rmtree(path)

def make_folder(path):    
    ''' 
        创建文件夹
    '''
    if exists_file(path):
        return
    os.makedir(path)

def make_folders(path):    
    ''' 
        递归创建文件夹
    '''
    if exists_file(path):
        return
    os.makedirs(path)

def mkdirs(path, isFolder):
    ''' 
        递归创建文件夹
    '''
    if isFolder:
        fPath = path
    else:
        fPath = os.path.dirname(path)
    if not os.path.exists(fPath):
        os.makedirs(fPath)


def move(src,dst):    
    ''' 
        给文件或文件夹改名（可以改路径，但是不能覆盖目标文件）
    '''
    # os.rename(src,dst)
    shutil.move(src, dst)


def walk(path):    
    ''' 
        列举path下的所有文件、文件夹
    '''
    return os.walk(path)
    
def walk2(path):
    ''' 
        列举path下的所有文件、文件夹
    '''
    fpaths = []
    for pt, fl, fi in os.walk(path):
        for f in fi:
            p = os.path.join(pt, f)
            fpaths.append((pt, f))
    return fpaths


def get_folder_son(path):
    ''' 
        列举path下一层的所有文件、文件夹
    '''
    paths = os.listdir(path)
    pps = []
    for s in paths:
        p = '%s%s%s' % (path, os.sep, s)
        pps.append(p)
    return pps


def read_all_file(filePath, method = 'r'):
    ''' 
        读取所有文件，一次性读取所有内容，文件不存在返回None
        filePath：文件路径
        method：读取方式，'r'读取，'rb' 二进制方式读取
    '''
    if not exists_file(filePath = filePath):
        return None
    fh = open(filePath, method)
    try:
        c = fh.read()
        return c
    finally:
        fh.close()


def read_all_lines_file(filePath, method = 'r'):
    ''' 
        读取所有文件，一次性读取所有内容， 文件不存在返回None
        filePath：文件路径
        method：读取方式，'r'读取，'rb' 二进制方式读取
    '''
    if not exists_file(filePath = filePath):
        return None
    fh = open(filePath, method)
    try:
        c = fh.readlines()
        return c
    finally:
        fh.close()


def read_line_file(filePath, method = 'r', callBack = None):
    ''' 
        读取所有文件，一次性读取所有内容， 文件不存在返回None
        filePath：文件路径
        method：读取方式，'r'读取，'rb' 二进制方式读取
        callBack：每行读取的回调函数，有两个传入参数，行索引和行内容
    '''
    if callBack == None:
        return
    if not exists_file(filePath = filePath):
        return

    fh = open(filePath, method)
    try:
        limit = 10000
        lineIndex = 0
        while True:  
            lines = fh.readlines(limit)
            if not lines:
                break
            for line in lines:
                callBack(lineIndex, line)
                lineIndex += 1
    finally:
        fh.close()

# while 1:
#     lines = file.readlines(100000)
#     if not lines:
#         break
#     for line in lines:
#         pass # do something

def write_file(filePath, content, method = 'w'):
    ''' 
        写文件 
        filePath：文件路径
        content：文件内容
        method：写入方式，'w'覆盖写，'a' 续写，'wb' 二进制覆盖写
    '''
    if type(content) != unicode:
        fh = open(filePath, method)
    else:
        fh = codecs.open(filePath, method, 'UTF-8')
    try:
        fh.write(content)
    except:
        print traceback.format_exc()
    finally:
        fh.close()


def get_file_folder_path(path):
    ''' 
        获取文件所存放文件夹：
        path：文件路径，可使用__file__
    '''
    path = os.path.split(os.path.realpath(path))[0]
    return path

def get_file_folder(path):
    '''
        获取文件所存放文件夹：
        path：文件路径，可使用__file__
    '''
    return os.path.dirname(path)

def get_file_name(path):
    '''
        获取文件名：
        path：文件路径，可使用__file__
    '''
    return os.path.basename(path)


def get_url_file_name(path):
    '''
        获取文件名：
        path：文件路径，可使用__file__
    '''
    return os.path.basename(path.split('?')[0])

def get_file_suffix(path):
    '''
        获取文件后缀
        path：文件路径，可使用__file__
    '''
    return os.path.splitext(path)[1][1:]


def get_folder_sep():
    ''' 
        获取操作系统文件路径分隔符
    '''
    return os.sep


def get_line_sep():
    ''' 
        获取操作系统换行分隔符
    '''
    return os.linesep


def get_path_sep():
    ''' 
        获取操作系统目录分隔符，windows中是 ;，PATH里会用到
    '''
    return os.pathsep


def get_ext_sep():
    ''' 
        获取操作系统扩展名分隔符，windows中是 .
    '''
    return os.extsep


def md5_file(path):
    m = md5()
    a_file = open(path, 'rb')    #需要使用二进制格式读取文件内容
    try:
        m.update(a_file.read())
        return m.hexdigest()
    except:
        print traceback.format_exc()
    finally:
        a_file.close()
    

def get_folder_sizes(path):
    ''' 获取目录下子文件、目录的大小 '''
    cmd = 'du -sb %s/*' % (path)

    pss = os.popen(cmd).readlines()

    fileSizes = {}
    for l in pss:
        ll = l.strip().split('\t')
        size = int(ll[0])
        code = ll[1].replace(path+os.sep, '')
        fileSizes[code] = size

    return fileSizes

def get_file_md5(path):
    ''' 获取文件md5 '''
    cmd = 'md5sum %s ' % (path)
    print cmd
    md5s = os.popen(cmd).readlines()    
    print md5s
    for m in md5s:
        l = m.strip()
        ls = l.split('  ')
        if len(ls) != 2:
            continue

        return ls[0].strip()

if __name__ == '__main__':
    print '1'