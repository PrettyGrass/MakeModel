# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


class BaseInfo:
    def __init__(self):
        self.remark = '注释'   # 类注释


class ClassInfo(BaseInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        self.fileHeaderRemark = '文件头注释'  # 文件注释
        self.remark = '类注释'  # 方法注释

        self.superClazz = None      # 父类名
        self.name = ''              # 类名
        self.methods = []           # 方法列表
        self.props = []             # 属性
        self.imports = []           # 引入关系 (内部类没有)
        self.innerImports = []      # 内部引入关系 oc

        self.hostClass = None       # 依附的类, 该值不为空, 说明该类寄生于别的类文件中
        self.innerClass = []        # 内部类, java 支持, swift 支持
        self.inFileClass = []       # 同一个文件并存多类, swift 支持 oc 支持
        self.model = None           # 对应的数据模型, 用于精细化类生成


class MethodInfo(BaseInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        self.remark = '方法注释'    # 方法注释
        self.type = 0               # 0实例方法 1类方法
        self.retType = 'void'       # 返回值类型
        self.name = ''              # 函数名
        self.params = []            # 参数表
        self.bodyLines = []         # 实现


class PropInfo(BaseInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        self.remark = '属性注释'     # 方法注释
        self.type = ''              # 类型
        # 子类型,数组, 字典对象使用 list[object] dict(object1: object2)
        self.subTypes = []
        self.name = ''              # 名字
