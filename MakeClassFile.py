# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


class MakeClassFile:
    # 构造方法
    def __init__(self, clazz, model):
        self.clazz = clazz
        self.model = model

    # 开始
    def start(self):
        assert '各端需要实现自己的类生成方法'

    # 创建头部注释
    def createHeaderRemark(self, indent=0):
        pass

    # 创建类注释
    def createClassRemark(self, indent=0):
        pass

    # 创建接口
    def createInterface(self, indent=0):
        pass

    # 创建实现
    def createImpl(self, indent=0):
        pass

    # 创建属性
    def createProp(self=0):
        pass

    # 创建方法
    def createFunc(self=0):
        pass
