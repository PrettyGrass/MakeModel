# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

class ClassInfo():
    def __init__(self):
        self.name = ''
        self.method = []
        self.props = []
        self.imports = []
        self.innerClass = []


class MethodInfo():
    def __init__(self):
        # 作用域,
        self.type = 0
        self.retType = 'void'
        self.name = ''
        self.params = []


class PropInfo():
    def __init__(self):
        # 作用域, 内存管理方式
        self.type = ''
        self.subTypes = [] # 数组, 字典对象使用 list[object] dict(object1: object2)
        self.name = ''

