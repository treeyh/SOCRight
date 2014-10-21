#-*- encoding: utf-8 -*-

import os



def write_file(filePath, content, method = 'a'):
    ''' 
        写文件 
        filePath：文件路径
        content：文件内容
        method：写入方式，'w'覆盖写，'a' 续写，'wb' 二进制覆盖写
    '''
    fh = open(filePath, method)
    try:
        fh.write(content)
    finally:
        fh.close()