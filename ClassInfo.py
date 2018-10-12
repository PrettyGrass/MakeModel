# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


class BaseInfo:
    def __init__(self):
        pass


class ClassInfo(BaseInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        self.name = ''              # 类名
        self.methods = []           # 方法列表
        self.props = []             # 属性
        self.imports = []           # 引入关系 (内部类没有)
        self.innerClass = []        # 内部类, 部分语言不支持

        self.hostClass = None       # 依附的类, 该值不为空, 说明该类寄生于别的类文件中
        self.innerClass = []        # 内部类, java 支持, swift 支持
        self.inFileClass = []       # 同一个文件并存多类, swift 支持 oc 支持


class MethodInfo(BaseInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        self.type = 0               # 实例方法 类方法
        self.retType = 'void'       # 返回值类型
        self.name = ''              # 函数名
        self.params = []            # 参数表


class PropInfo(BaseInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        self.type = ''              # 类型
        self.subTypes = []          # 子类型,数组, 字典对象使用 list[object] dict(object1: object2)
        self.name = ''              # 名字
