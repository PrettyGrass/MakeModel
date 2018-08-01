# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

# 接口信息
class APIInfo():
    def __init__(self):
        self.name = ''
        self.method = ''  # get post..
        self.protocol = '' # https / http
        self.host = ''  # 主机
        self.path = ''  # 路径
        self.headers = {}  # 请求头
        self.params = []  # 请求参数
        self.responses = []  # 响应数据(字符json)


# 接口组
class APIGroupInfo():
    def __init__(self):
        self.name = ''
        self.description = ''
        self.apis = []


# 输入参数
class ParamsInfo():
    def __init__(self):
        self.type = ''  # get post restful
        self.name = ''
        self.paramType = 'string'
