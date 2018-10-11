# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


from ClassInfo import *

from conf import Conf


# 解析api数据
class TransAPIModel2ClassInfo():
    def __init__(self, apiGroups):
        self.apiGroups = apiGroups
        self.conf = Conf()

    def trans(self):
        for index in range(len(self.apiGroups)):
            apiGroup = self.apiGroups[index]

    def transSingleGroup(self, apiGroup):
        apiClazz = None
        for index in range(len(apiGroup.apis)):
            api = apiGroup.apis[index]
            apiClazz = ClassInfo()

        return apiClazz
