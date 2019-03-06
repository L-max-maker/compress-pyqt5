#!/usr/bin/env python3
# coding:utf-8
# Author: wangping@www.yuanrenxue.com

import time
import os
import traceback
import zipfile

g_log = None

#计算目录大小
def get_dir_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

#计算文件大小
def get_file_size(path):
    return os.path.getsize(path)

#压缩文件
def zip_file(path):
    zip = zipfile.ZipFile(path.split('.')[0]+'.zip','w',zipfile.ZIP_DEFLATED)
    #zip.write()
    zip.write(path, os.path.basename(path))
    #zip.write(path, path)
    zip.close()
    return path.split('.')[0] +'.zip'

#压缩目录
def zip_dir(path):
    zip = zipfile.ZipFile(path +'.zip','w',zipfile.ZIP_DEFLATED)
    for root,dirs,files in os.walk(path):
        print(root,dirs)
        for file in files:
            whole_path = os.path.join(root, file)
            zip.write(whole_path,whole_path[len(path)+1:])
    zip.close()
    return path +'.zip'

#把文件字节大小转换为K,M,G等单位
def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def yzx_zip(path):
    if os.path.isdir(path):
        zip_dir_path = zip_dir(path)
        before_zip_size = sizeof_fmt(get_dir_size(path))
        after_zip_size = sizeof_fmt(get_file_size(zip_dir_path))
        return zip_dir_path,before_zip_size,after_zip_size
    else:
        zip_file_path = zip_file(path)
        before_zip_size = sizeof_fmt(get_file_size(path))
        after_zip_size = sizeof_fmt(get_file_size(zip_file_path))
        return zip_file_path,before_zip_size,after_zip_size

def yzx_unzip(path):
    new_dir = path.split('.')[0]
    print('new_dir:',new_dir)
    os.mkdir(new_dir)
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(new_dir)
    zip_ref.close()
    return path.split('.')[0]


if __name__ == '__main__':
    #from sys import argv
    zip_file('D:/doc/111.txt')

