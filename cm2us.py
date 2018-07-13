#!/bin/python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


import re, sys, json
 
# 驼峰转下划线
def camelToUnderlines(x):
    prefix = re.split('([a-zA-Z])', x, 1)[0]
    x = re.sub('([A-Z])', lambda match : '_' + match.group().lower(), x)
    if x[0] == '_':
        x = x[1:]
    return prefix + x
    
# 下划线转大驼峰
def underlinesToCamel(x):

    prefix = re.split('([a-zA-Z])', x, 1)[0]

    if x[0] != '_':
        x = '_' + x
    x = re.sub('_([a-z])', lambda match: match.group(1).upper(), x)
    if x[0] == '_':
        x = x[1:]
    return prefix + x

def transStr(file_path, cmToUs_or_usToCm):
    print cmToUs_or_usToCm
    f = open(file_path, 'r')
    if cmToUs_or_usToCm == '1':
        print "驼峰转下划线"
        for line in f.readlines():
            print camelToUnderlines(line.strip())
    elif cmToUs_or_usToCm == '0':
        print "下划线转大驼峰"
        for line in f.readlines():
            print underlinesToCamel(line.strip())

    f.close()

if __name__ == '__main__':
    style = sys.argv[2]
    transStr(sys.argv[1], style)