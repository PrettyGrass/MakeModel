# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


import util
from ClassInfo import *


# 模型信息
class ModelInfo:
    def __init__(self):
        self.name = ''      # 模型名
        self.fields = []    # FieldInfo
        self.subModels = [] # 子模型
        self.remark = ''

    def getRefClassType(self, ref):
        for model in self.subModels:
            if ref == model.ref:
                return model

# 字段
class FieldInfo:
    def __init__(self):
        self.ref = None
        self.name = ''
        self.type = ''
        self.subType = ''
        self.remark = ''
        self.testValue = ''