# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


class MakeClassFile():
    # 构造方法
    def __init__(self, clazz, model):
        self.clazz = clazz
        self.model = model

    # 开始
    def run(self):
        print '需要自己实现对应的生成过程'

    # 创建头部注释
    def createBeginRemark(self, lines):
        pass

    # 创建头部注释
    def createEndRemark(self, lines):
        pass

    # 创建类注释
    def createClassRemark(self, lines):
        pass

    # 创建接口
    def createInterfaceBegin(self, lines):
        pass

    # 创建接口
    def createInterfaceBody(self, lines):
        pass

    # 创建接口
    def createInterfaceEnd(self, lines):
        pass

    # 创建实现
    def createImplBegin(self, lines):
        pass

    # 创建实现
    def createImplBody(self, lines):
        pass

    # 创建实现
    def createImplEnd(self, lines):
        pass

    # 创建属性
    def createProp(self, lines, prop):
        pass

    # 创建方法
    def createFuncBegin(self, lines, func):
        pass

    # 创建方法
    def createFuncBody(self, lines, func):
        pass

    # 创建方法
    def createFuncEnd(self, lines, func):
        pass
