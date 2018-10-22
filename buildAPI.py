# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

from OCApi import *
from ObjectiveC import ObjectiveC
from ObjectiveC import TransAPIModel2OCClass
from ParseApiJson import *
import os

if __name__ == '__main__':
    wkPath = os.path.dirname('.')  # 当前的目录
    wkPath = os.path.abspath(wkPath)
    print 'wk:', wkPath

    pm = ParseApiJson(wkPath)
    ms = pm.apiGroups()

    print 'api组:', len(ms)
    # 老的
    # ocApi = OCApi(wkPath, ms)
    # ocApi.init()
    # ocApi.build()

    trans = TransAPIModel2OCClass(ms)
    trans.makrClazzList(trans.trans(), os.path.join(wkPath, 'Product', 'ocapi'))

