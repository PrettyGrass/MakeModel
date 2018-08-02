# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import os, OC, java, util, re, sys
from ClassInfo import *
from OCApi import *
from ParseApiJson import *

sys.path.append('./conf')
from conf import Conf



if __name__ == '__main__':
    wkPath = os.path.dirname('.')  # 当前的目录
    wkPath = os.path.abspath(wkPath)
    print 'wk:', wkPath

    pm = ParseApiJson(wkPath)
    ms = pm.apiGroups()

    print 'api组:', len(ms)
    ocApi = OCApi(wkPath, ms)
    ocApi.init()
    ocApi.build()
