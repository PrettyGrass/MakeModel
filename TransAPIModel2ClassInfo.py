# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


from ClassInfo import *

from conf import Conf
from ClassInfo import ClassInfo


# 解析api数据
class TransAPIModel2ClassInfo():
    def __init__(self, apiGroups):
        self.apiGroups = apiGroups
        self.conf = Conf()

    def trans(self):
        clazzs = []
        for index in range(len(self.apiGroups)):
            apiGroup = self.apiGroups[index]
            clazzs.append(self.transSingleGroup(apiGroup))

        return clazzs

    def transSingleGroup(self, apiGroup):
        apiClazz = ClassInfo()
        apiClazz.name = apiGroup.enName
        for index in range(len(apiGroup.apis)):
            api = apiGroup.apis[index]
            method = MethodInfo()
            method.name = api.name
            apiClazz.methods.append(method)

        return apiClazz
