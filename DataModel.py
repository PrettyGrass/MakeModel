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

# 字段
class FieldInfo:
    def __init__(self):
        self.ref = None
        self.name = ''
        self.type = ''
        self.subType = ''