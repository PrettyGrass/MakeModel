# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


import util
from ClassInfo import *


# 接口信息
class APIInfo():
    def __init__(self):
        self.name = ''
        self.enName = ''
        self.method = ''  # get post..
        self.protocol = ''  # https / http
        self.host = ''  # 主机
        self.path = ''  # 路径
        self.paths = []  # 路径
        self.headers = {}  # 请求头
        self.params = []  # 请求参数
        self.responses = []  # 响应数据(字符json)

        self.classMethod = MethodInfo()


# 接口组
class APIGroupInfo():
    def __init__(self):
        self.clazz = ClassInfo()
        self.name = ''
        self.enName = ''
        self.description = ''
        self.apis = []

    def getFileName(self, prefix=''):
        return prefix + util.firstUpper(self.enName) + 'API'


# 输入参数
class ParamsInfo():
    def __init__(self):
        self.type = ''  # get post restful
        self.name = ''
        self.paramType = 'string'
