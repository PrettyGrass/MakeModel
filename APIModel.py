# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


import util
from ClassInfo import *


# 接口信息
class APIInfo:
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

    def getMethodName(self):
        funcName = ''
        use = False
        if self.method.lower() not in ['get', 'post']:
            funcName = self.method.lower()
            use = True

        for index in range(len(self.paths)):
            p = self.paths[index]
            if index == 0 and util.isNumberBegin(p):
                # 开头是数字忽略
                continue
            if use:
                p = util.firstUpper(p)

            if p.find(':') == -1:
                # .不能做方法名
                p = p.replace('.', '_')
                funcName += p
                use = True

        return funcName


# 接口组
class APIGroupInfo:
    def __init__(self):
        self.clazz = ClassInfo()
        self.name = ''
        self.enName = ''
        self.description = ''
        self.apis = []

    def getFileName(self, prefix=''):
        return prefix + util.firstUpper(self.enName) + 'API'


# 输入参数
class ParamsInfo:
    def __init__(self):
        self.type = ''  # get post restful
        self.name = ''
        self.paramType = 'string'
